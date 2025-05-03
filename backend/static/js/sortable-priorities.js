// Initialize Sortable.js for the priority list
document.addEventListener('DOMContentLoaded', () => {
    const priorityList = document.getElementById('prioritats-list');

    if (priorityList) {
        new Sortable(priorityList, {
            animation: 150,
            onEnd: () => {
                // Update the hidden input with the new order
                const order = Array.from(priorityList.children).map(item => item.dataset.id);
                document.getElementById('prioritats_ordre').value = order.join(',');
            }
        });
    }
});