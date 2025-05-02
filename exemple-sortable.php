<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exemple de Categories Ordenables</title>
    <style>
        .categoria {
            padding: 1rem;
            margin: 0.5rem 0;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .categoria:hover {
            background-color: #f8f9fa;
        }

        .contenidor-categories {
            max-width: 600px;
            margin: 2rem auto;
            padding: 1rem;
        }

        .handle {
            margin-right: 1rem;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="contenidor-categories">
        <h2>Categories Ordenables</h2>
        <div id="categories-list">
            <div class="categoria sortable-item" data-id="1">
                <span class="handle sortable-handle">☰</span> Categoria 1
            </div>
            <div class="categoria sortable-item" data-id="2">
                <span class="handle sortable-handle">☰</span> Categoria 2
            </div>
            <div class="categoria sortable-item" data-id="3">
                <span class="handle sortable-handle">☰</span> Categoria 3
            </div>
            <div class="categoria sortable-item" data-id="4">
                <span class="handle sortable-handle">☰</span> Categoria 4
            </div>
        </div>
    </div>

    <script src="sortable-categories.js"></script>
    <script>
        // Inicialitzar el sistema d'ordenació
        const sortable = new SortableCategories('categories-list', {
            itemClass: 'sortable-item',
            handleClass: 'sortable-handle',
            onOrderChange: (newOrder) => {
                console.log('Nou ordre:', newOrder);
                // Aquí pots implementar la lògica per guardar el nou ordre
            }
        });
    </script>
</body>
</html>