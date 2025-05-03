<<<<<<< HEAD
class SortableCategories {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) throw new Error('Contenidor no trobat');

        this.options = {
            itemClass: options.itemClass || 'sortable-item',
            handleClass: options.handleClass || 'sortable-handle',
            dragClass: options.dragClass || 'is-dragging',
            onOrderChange: options.onOrderChange || null
        };

        this.init();
    }

    init() {
        this.items = this.container.getElementsByClassName(this.options.itemClass);
        Array.from(this.items).forEach(item => {
            item.setAttribute('draggable', 'true');
            
            // Afegir listeners per drag & drop
            item.addEventListener('dragstart', (e) => this.handleDragStart(e));
            item.addEventListener('dragend', (e) => this.handleDragEnd(e));
            item.addEventListener('dragover', (e) => this.handleDragOver(e));
            item.addEventListener('drop', (e) => this.handleDrop(e));
        });
    }

    handleDragStart(e) {
        const item = e.target;
        item.classList.add(this.options.dragClass);
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', Array.from(this.items).indexOf(item));
    }

    handleDragEnd(e) {
        e.target.classList.remove(this.options.dragClass);
    }

    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }

    handleDrop(e) {
        e.preventDefault();
        const item = e.target.closest(`.${this.options.itemClass}`);
        if (!item) return;

        const oldIndex = parseInt(e.dataTransfer.getData('text/plain'));
        const newIndex = Array.from(this.items).indexOf(item);

        if (oldIndex !== newIndex) {
            this.reorderItems(oldIndex, newIndex);
            if (this.options.onOrderChange) {
                this.options.onOrderChange(this.getOrder());
            }
        }
    }

    reorderItems(oldIndex, newIndex) {
        const items = Array.from(this.items);
        const [movedItem] = items.splice(oldIndex, 1);
        items.splice(newIndex, 0, movedItem);

        // Actualitzar l'ordre al DOM
        items.forEach(item => this.container.appendChild(item));
    }

    getOrder() {
        return Array.from(this.items).map(item => ({
            id: item.dataset.id,
            order: Array.from(this.items).indexOf(item)
        }));
    }

    // Mètode per actualitzar l'ordre manualment
    updateOrder(newOrder) {
        newOrder.forEach((id, index) => {
            const item = Array.from(this.items).find(item => item.dataset.id === id);
            if (item) this.container.appendChild(item);
        });
    }
}

// Estils CSS per defecte
const style = document.createElement('style');
style.textContent = `
    .sortable-item {
        cursor: move;
        user-select: none;
        transition: background-color 0.2s ease;
    }

    .sortable-item.is-dragging {
        opacity: 0.5;
        background-color: #f0f0f0;
    }

    .sortable-handle {
        cursor: move;
    }
`;
=======
class SortableCategories {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) throw new Error('Contenidor no trobat');

        this.options = {
            itemClass: options.itemClass || 'sortable-item',
            handleClass: options.handleClass || 'sortable-handle',
            dragClass: options.dragClass || 'is-dragging',
            onOrderChange: options.onOrderChange || null
        };

        this.init();
    }

    init() {
        this.items = this.container.getElementsByClassName(this.options.itemClass);
        Array.from(this.items).forEach(item => {
            item.setAttribute('draggable', 'true');
            
            // Afegir listeners per drag & drop
            item.addEventListener('dragstart', (e) => this.handleDragStart(e));
            item.addEventListener('dragend', (e) => this.handleDragEnd(e));
            item.addEventListener('dragover', (e) => this.handleDragOver(e));
            item.addEventListener('drop', (e) => this.handleDrop(e));
        });
    }

    handleDragStart(e) {
        const item = e.target;
        item.classList.add(this.options.dragClass);
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', Array.from(this.items).indexOf(item));
    }

    handleDragEnd(e) {
        e.target.classList.remove(this.options.dragClass);
    }

    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }

    handleDrop(e) {
        e.preventDefault();
        const item = e.target.closest(`.${this.options.itemClass}`);
        if (!item) return;

        const oldIndex = parseInt(e.dataTransfer.getData('text/plain'));
        const newIndex = Array.from(this.items).indexOf(item);

        if (oldIndex !== newIndex) {
            this.reorderItems(oldIndex, newIndex);
            if (this.options.onOrderChange) {
                this.options.onOrderChange(this.getOrder());
            }
        }
    }

    reorderItems(oldIndex, newIndex) {
        const items = Array.from(this.items);
        const [movedItem] = items.splice(oldIndex, 1);
        items.splice(newIndex, 0, movedItem);

        // Actualitzar l'ordre al DOM
        items.forEach(item => this.container.appendChild(item));
    }

    getOrder() {
        return Array.from(this.items).map(item => ({
            id: item.dataset.id,
            order: Array.from(this.items).indexOf(item)
        }));
    }

    // Mètode per actualitzar l'ordre manualment
    updateOrder(newOrder) {
        newOrder.forEach((id, index) => {
            const item = Array.from(this.items).find(item => item.dataset.id === id);
            if (item) this.container.appendChild(item);
        });
    }
}

// Estils CSS per defecte
const style = document.createElement('style');
style.textContent = `
    .sortable-item {
        cursor: move;
        user-select: none;
        transition: background-color 0.2s ease;
    }

    .sortable-item.is-dragging {
        opacity: 0.5;
        background-color: #f0f0f0;
    }

    .sortable-handle {
        cursor: move;
    }
`;
>>>>>>> 1808252 (Millores DB + Front)
document.head.appendChild(style);