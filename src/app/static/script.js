import {exportDeckFile, generateWordsData} from './api.js';

/**
 * @typedef {import('./api.js').WordWithHints} WordWithHints
 */

/**
 * @param {string} language
 * @param {WordWithHints[]} wordsWithHints
 */
async function sendCardsRequest(language, wordsWithHints) {
    const wordsData = await generateWordsData(language, wordsWithHints);
    const deckFile = await exportDeckFile(language, wordsData);
    downloadBlob(deckFile, getGeneratedAnkiFileName(language));
}

/**
 * @param {Blob} blob
 * @param {string} fileName
 */
function downloadBlob(blob, fileName) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}

/**
 * @typedef {Object} VocabItem
 * @property {string} raw
 * @property {string} word
 * @property {?string} hint
 */

/**
 * @param {string} raw
 * @param {boolean} [showAlert=true]
 * @returns {?VocabItem}
 */
function parseWordItem(raw, showAlert = true) {
    const trimmed = raw.trim();
    if (!trimmed) {
        return null;
    }
    const parts = trimmed.split('=').map(part => part.trim());
    if (parts.length > 2 || (parts.length === 2 && parts[1] === '') || parts[0] === '') {
        if (showAlert) {
            alert("Invalid word format: " + trimmed);
        }
        return null;
    }
    return {
        raw: trimmed,
        word: parts[0],
        hint: parts.length === 2 ? parts[1] : null,
    };
}

/**
 * @param {VocabItem} item
 * @returns {WordWithHints}
 */
function itemToWordWithHints(item) {
    const result = {
        word: item.word,
    };
    if (item.hint) {
        result.hints = { translated_ru: item.hint };
    }
    return result;
}

/**
 * @param {string} language
 * @returns {string}
 */
function getGeneratedAnkiFileName(language) {
    const languagePart = language === 'de' ? "german" : "english"
    const localDateTimePart = formatLocalDateTime();
    return `to_import_${languagePart}_anki_generated_${localDateTimePart}.apkg`;
}

/**
 * @returns {string}
 */
function formatLocalDateTime() {
    const date = new Date()
    const pad = n => String(n).padStart(2, '0');
    return [
        date.getFullYear(),
        pad(date.getMonth() + 1),
        pad(date.getDate())
    ].join('-') + '_' + [
        pad(date.getHours()),
        pad(date.getMinutes()),
        pad(date.getSeconds())
    ].join('-');
}

document.addEventListener('alpine:init', () => {
    Alpine.data('ankiApp', () => ({
        language: 'de',
        inputValue: '',
        items: [],
        loading: false,
        placeholders: {
            de: "Katze = кошка",
            en: "cat = кошка",
        },

        get canGenerate() {
            return !this.loading && (this.items.length > 0 || this.inputValue.trim() !== '');
        },

        scrollToBottom() {
            this.$nextTick(() => {
                const stackEl = document.querySelector('.vocab-stack');
                if (stackEl) {
                    stackEl.scrollTop = stackEl.scrollHeight;
                }
            });
        },

        addWord() {
            const raw = this.inputValue.trim();
            if (!raw) {
                return;
            }
            const parsed = parseWordItem(raw, true);
            if (!parsed) {
                return;
            }
            this.items.push(parsed);
            this.inputValue = '';
            this.scrollToBottom();
        },

        removeItem(index) {
            this.items.splice(index, 1);
        },

        handleBackspace(event) {
            if (this.inputValue === '' && this.items.length > 0) {
                event.preventDefault();
                const lastItem = this.items.pop();
                this.inputValue = lastItem.raw;
                // Move cursor to the end of the restored word for editing
                this.$nextTick(() => {
                    const el = event.target;
                    if (el && typeof el.setSelectionRange === 'function') {
                        const len = this.inputValue.length;
                        el.setSelectionRange(len, len);
                    }
                });
            }
        },

        handlePaste(event) {
            const pasteText = (event.clipboardData || window.clipboardData)?.getData('text');
            if (!pasteText) {
                return;
            }

            if (pasteText.includes('\n') || pasteText.includes('\r')) {
                event.preventDefault();
                const lines = pasteText
                    .split(/\r?\n/)
                    .map(line => line.trim())
                    .filter(line => line.length > 0);

                const parsedItems = [];
                const invalidLines = [];
                for (const line of lines) {
                    const parsed = parseWordItem(line, false);
                    if (parsed) {
                        parsedItems.push(parsed);
                    } else {
                        invalidLines.push(line);
                    }
                }

                if (invalidLines.length > 0) {
                    alert("Invalid word format in pasted text. Nothing was added:\n" + invalidLines.join('\n'));
                    return;
                }

                this.items.push(...parsedItems);
                this.scrollToBottom();
            }
        },

        async onGenerateButtonClick() {
            if (!this.canGenerate) {
                return;
            }

            if (this.inputValue.trim() !== '') {
                const parsed = parseWordItem(this.inputValue.trim(), true);
                if (!parsed) {
                    return;
                }
                this.items.push(parsed);
                this.inputValue = '';
            }

            if (this.items.length === 0) {
                return;
            }

            const wordsWithHints = this.items.map(itemToWordWithHints);

            this.loading = true;

            try {
                await sendCardsRequest(this.language, wordsWithHints);
                this.items = [];
                this.inputValue = '';
            } catch (error) {
                console.error(error);
                alert("Something went wrong. Inspect app logs for more details. 🥷");
            } finally {
                this.loading = false;
            }
        },
    }));
});
