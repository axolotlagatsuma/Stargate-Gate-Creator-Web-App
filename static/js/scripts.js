function createGrid() {
    const size = document.getElementById('size').value;
    const gridContainer = document.getElementById('grid-container');
    gridContainer.innerHTML = '';

    for (let i = 0; i < size; i++) {
        const row = document.createElement('div');
        row.className = 'grid-row';

        for (let j = 0; j < size; j++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.onclick = () => selectCell(cell);
            row.appendChild(cell);
        }

        gridContainer.appendChild(row);
    }
}

function selectCell(cell) {
    if (cell.classList.contains('selected')) {
        cell.classList.remove('selected');
        cell.style.backgroundImage = '';
        cell.dataset.block = '';
    } else {
        const block = prompt('Enter block name (corresponds to your texture filename):');
        if (block) {
            cell.classList.add('selected');
            cell.style.backgroundImage = `url('/static/images/${block}.png')`;
            cell.dataset.block = block;
        }
    }
}

document.getElementById('gate-form').onsubmit = function () {
    const gridData = [];
    document.querySelectorAll('.grid-row').forEach(row => {
        const rowData = [];
        row.querySelectorAll('.grid-cell').forEach(cell => {
            rowData.push(cell.dataset.block || 'AIR');
        });
        gridData.push(rowData);
    });
    const gridInput = document.createElement('input');
    gridInput.type = 'hidden';
    gridInput.name = 'grid_data[]';
    gridInput.value = JSON.stringify(gridData);
    this.appendChild(gridInput);
};
