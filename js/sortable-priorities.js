class SortablePriorities {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.initializeSortable();
    }

    initializeSortable() {
        let items = this.container.querySelectorAll('.priority-item');
        let draggedItem = null;

        items.forEach(item => {
            // Afegir tooltip
            item.setAttribute('title', item.dataset.description);

            // Gestionar events de drag & drop
            item.addEventListener('dragstart', (e) => {
                draggedItem = item;
                setTimeout(() => item.classList.add('dragging'), 0);
            });

            item.addEventListener('dragend', () => {
                item.classList.remove('dragging');
                this.updatePriorities();
            });

            item.addEventListener('dragover', (e) => {
                e.preventDefault();
                if (item !== draggedItem) {
                    const rect = item.getBoundingClientRect();
                    const y = e.clientY - rect.top;
                    const height = rect.height;
                    
                    if (y < height / 2) {
                        item.parentNode.insertBefore(draggedItem, item);
                    } else {
                        item.parentNode.insertBefore(draggedItem, item.nextSibling);
                    }
                }
            });
        });
    }

    updatePriorities() {
        const priorities = [];
        this.container.querySelectorAll('.priority-item').forEach((item, index) => {
            priorities.push({
                id: item.dataset.id,
                name: item.textContent.trim(),
                order: index + 1
            });
        });

        // Actualitzar el camp ocult amb les prioritats ordenades
        const hiddenInput = document.getElementById('prioritats_ordre');
        if (hiddenInput) {
            hiddenInput.value = JSON.stringify(priorities);
        }
    }
}