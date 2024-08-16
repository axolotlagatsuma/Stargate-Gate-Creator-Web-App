document.addEventListener('DOMContentLoaded', () => {
    loadTextures();
});

function loadTextures() {
    fetch('/static/images/textures.json')
        .then(response => response.json())
        .then(textures => {
            const textureList = document.getElementById('texture-list');
            textures.forEach(texture => {
                const img = document.createElement('img');
                img.src = `/static/images/${texture}`;
                img.className = 'texture';
                img.onclick = () => selectTexture(texture);
                textureList.appendChild(img);
            });
        })
        .catch(error => console.error('Error loading textures:', error));
}

function selectTexture(texture) {
    const selectedCell = document.querySelector('.grid-cell.selected');
    if (selectedCell) {
        selectedCell.style.backgroundImage = `url('/static/images/${texture}')`;
        selectedCell.dataset.block = texture;
        closeModal();
    }
}

function openModal(cell) {
    document.querySelector('.grid-cell.selected')?.classList.remove('selected');
    cell.classList.add('selected');
    document.getElementById('texture-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('texture-modal').style.display = 'none';
}

function createGrid() {
    const width = document.getElementById('width').value;
    const height = document.getElementById('height').value;
    const gridContainer = document.getElementById('grid-container');
    gridContainer.innerHTML = '';

    for (let i = 0; i < height; i++) {
        const row = document.createElement('div');
        row.className = 'grid-row';

        for (let j = 0; j < width; j++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.onclick = () => openModal(cell);
            row.appendChild(cell);
        }

        gridContainer.appendChild(row);
    }
}

document.getElementById('gate-form').onsubmit = function () {
    const width = document.getElementById('width').value;
    const height = document.getElementById('height').value;
    const gridData = [];

    for (let i = 0; i < height; i++) {
        const rowData = [];
        for (let j = 0; j < width; j++) {
            const cell = document.querySelector(`.grid-row:nth-child(${i + 1}) .grid-cell:nth-child(${j + 1})`);
            rowData.push(cell?.dataset.block || 'AIR');
        }
        gridData.push(rowData);
    }

    const gridInput = document.getElementById('grid_data');
    gridInput.value = JSON.stringify(gridData);

    return true; // Ensure form submission continues
};
