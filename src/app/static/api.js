/**
 * @typedef {Object} WordHints
 * @property {string} translated_ru
 *
 * @typedef {Object} WordWithHints
 * @property {string} word
 * @property {?WordHints} hints
 */

/**
 * @param {string} url
 * @param {Object} body
 * @returns {Promise<Response>}
 */
async function postJson(url, body) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
}

/**
 * @param {string} language
 * @param {WordWithHints[]} wordsWithHints
 * @returns {Promise<Object[]>}
 */
export async function generateWordsData(language, wordsWithHints) {
    return Promise.all(wordsWithHints.map((wordWithHints) => generateWordData(language, wordWithHints)));
}

/**
 * @param {string} language
 * @param {WordWithHints} wordWithHints
 * @returns {Promise<Object>}
 */
export async function generateWordData(language, wordWithHints) {
    const response = await postJson('/api/generateWordData', {
        language: language,
        word: wordWithHints.word,
        hints: wordWithHints.hints,
    });
    return response.json();
}

/**
 * @param {string} language
 * @param {Object[]} words
 * @returns {Promise<Blob>}
 */
export async function exportDeckFile(language, words) {
    const response = await postJson('/api/exportDeckFile', {
        language: language,
        words: words,
    });
    return response.blob();
}
