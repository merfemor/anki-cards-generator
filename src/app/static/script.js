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
 * @returns {?WordWithHints}
 */
function parseWordWithHint(word) {
    const parts = word.split('=').map(part => part.trim());
    const response = {
        word: parts[0],
    }
    if (parts.length === 2) {
        const translated_ru = parts[1];
        if (translated_ru === "") {
            alert("Invalid word format: " + word);
            return null;
        }
        response.hints = {translated_ru: translated_ru}
    }
    if (parts.length > 2) {
        alert("Invalid word format: " + word);
        return null;
    }
    return response;
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

/**
 * @param {string} wordsInput
 * @returns {?WordWithHints[]}
 */
function getConvertedValueOfWordsInputField(wordsInput) {
    const words = wordsInput
        .split('\n')
        .map(word => word.trim())
        .filter(word => word !== '')
        .map(parseWordWithHint);
    if (words.includes(null)) {
        return null;
    }
    return words;
}

document.addEventListener('alpine:init', () => {
    Alpine.data('ankiApp', () => ({
        language: 'de',
        words: '',
        loading: false,
        placeholders: {
            de: "Katze\nHund\nGeschwindigkeitsbeschränkung",
            en: "cat\ndog\ncapybara",
        },

        get canGenerate() {
            return !this.loading && this.words.trim() !== '';
        },

        async onGenerateButtonClick() {
            if (!this.canGenerate) {
                return;
            }
            const wordsWithHints = getConvertedValueOfWordsInputField(this.words.trim());
            if (wordsWithHints === null) {
                return;
            }

            this.loading = true;

            try {
                await sendCardsRequest(this.language, wordsWithHints);
                this.words = '';
            } catch (error) {
                console.error(error);
                alert("Something went wrong. Inspect app logs for more details. 🥷");
            } finally {
                this.loading = false;
            }
        },
    }));
});
