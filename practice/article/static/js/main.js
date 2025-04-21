document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const articleText = document.getElementById('articleText');
    const keywordsContainer = document.getElementById('keywords');
    const entitiesContainer = document.getElementById('entities');

    analyzeBtn.addEventListener('click', async function() {
        const text = articleText.value.trim();
        
        if (!text) {
            alert('Please enter some text to analyze');
            return;
        }

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();
            
            // Display keywords
            keywordsContainer.innerHTML = '';
            data.keywords.forEach(keyword => {
                const keywordElement = document.createElement('span');
                keywordElement.className = 'keyword';
                keywordElement.textContent = keyword;
                keywordsContainer.appendChild(keywordElement);
            });

            // Display entities
            entitiesContainer.innerHTML = '';
            data.entities.forEach(entity => {
                const entityElement = document.createElement('span');
                entityElement.className = 'entity';
                entityElement.textContent = `${entity.text} (${entity.label})`;
                entitiesContainer.appendChild(entityElement);
            });

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing the text');
        }
    });
}); 