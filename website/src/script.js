async function sendCardsRequest(language, wordsWithHints) {
  try {
    const requestBody = {
      words: wordsWithHints,
      language: language,
    };
    const response = await fetch('http://127.0.0.1:5000/api/generateCardsFile', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) throw new Error("Request failed");

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = language === 'de'
      ? "to_import_german_anki_generated.apkg"
      : "to_import_english_anki_generated.apkg";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    return true; // Success indicator
  } catch (error) {
    console.error(error);
    throw error; // Let the caller handle the error
  }
}

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

function setLoaderVisible(visible) {
  const loader = document.getElementById('loader');
  loader.style.display = visible ? 'block' : 'none';
}

function getConvertedValueOfWordsInputField() {
  const wordsInputFiled = document.getElementById('words');
  const wordsInput = wordsInputFiled.value.trim();

  if (!wordsInput) {
    alert("Enter at least one word.");
    return null;
  }
  const words = wordsInput.split('\n').map(word => word.trim()).map(parseWordWithHint);
  if (words.includes(null)) {
    return null;
  }
  return words;
}

function cleanWordsInputField() {
  const wordsInputFiled = document.getElementById('words');
  wordsInputFiled.value = '';
}

async function onGenerateButtonClick() {
  const language = document.getElementById('language').value;
  const wordsWithHints = getConvertedValueOfWordsInputField();
  if (wordsWithHints === null) {
    return;
  }
  setLoaderVisible(true);

  try {
    await sendCardsRequest(language, wordsWithHints);
    cleanWordsInputField();
  } catch {
    alert("Something went wrong.");
  } finally {
    setLoaderVisible(false);
  }
}

document.getElementById('generateBtn').addEventListener('click', onGenerateButtonClick);