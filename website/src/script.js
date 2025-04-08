async function sendCardsRequest(language, wordsArray) {
  try {
    // Select the appropriate endpoint based on the language
    const endpoint = language === 'de'
      ? 'http://127.0.0.1:5000/api/generateGermanCardsFile'
      : 'http://127.0.0.1:5000/api/generateEnglishCardsFile';

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ words: wordsArray })
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

// Event listener
document.getElementById('generateBtn').addEventListener('click', async () => {
  const language = document.getElementById('language').value;
  const wordsInputFiled = document.getElementById('words');
  const wordsInput = wordsInputFiled.value.trim();

  if (!wordsInput) {
    alert("Enter at least one word.");
    return;
  }

  // Convert the newline-separated words into a JSON array
  const wordsArray = wordsInput.split('\n').map(word => word.trim());

  const loader = document.getElementById('loader');
  loader.style.display = 'block';

  try {
    await sendCardsRequest(language, wordsArray);
    wordsInputFiled.value = '';
  } catch {
    alert("Something went wrong.");
  } finally {
    loader.style.display = 'none';
  }
});