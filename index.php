<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    header('Content-Type: application/json; charset=utf-8');

    // Netejar i preparar dades (pots afegir més validacions si cal)
    $dades = [
        // Informació Bàsica
        'ubicacio' => $_POST['ubicacio'] ?? '',
        'nacionalitat' => $_POST['nacionalitat'] ?? '',
        'data_inici' => $_POST['data_inici'] ?? '',
        'data_fi' => $_POST['data_fi'] ?? '',
        'pressupost' => $_POST['pressupost'] ?? '',
        'durada' => $_POST['durada'] ?? '',

        // Preferències Personals
        'interessos' => $_POST['interessos'] ?? [],
        'clima' => $_POST['clima'] ?? '',
        'green_travel' => $_POST['green_travel'] ?? '',
        'allotjament' => $_POST['allotjament'] ?? '',
        'activitat_fisica' => $_POST['activitat_fisica'] ?? '',
        'transport' => $_POST['transport'] ?? '',

        // Prioritats Ordenades
        'prioritats_ordre' => json_decode($_POST['prioritats_ordre'] ?? '[]', true),

        // Informació Addicional
        'idiomes' => $_POST['idiomes'] ?? '',
        'experiencia' => $_POST['experiencia'] ?? '',
        'restriccions_alimentaries' => $_POST['restriccions_alimentaries'] ?? [],
        'restriccions' => $_POST['restriccions'] ?? '',
        'evitar' => $_POST['evitar'] ?? '',
        'comentaris' => $_POST['comentaris'] ?? ''
    ];

    // Mostrar el JSON
    echo json_encode($dades, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}
?>

<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Formulari de Preferències de Viatge</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <style>
        .priority-item {
            cursor: move;
            user-select: none;
            padding: 1rem;
            margin-bottom: 0.5rem;
            background-color: #fff;
            border: 1px solid #dee2e6;
            border-radius: 0.25rem;
            transition: background-color 0.2s ease;
        }

        .priority-item:hover {
            background-color: #f8f9fa;
        }

        .priority-item.dragging {
            opacity: 0.5;
            background-color: #e9ecef;
        }

        .priority-item::before {
            content: '☰';
            margin-right: 0.5rem;
            color: #6c757d;
        }
        .step-indicator {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            position: relative;
        }

        .step-indicator::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 2px;
            background: #dee2e6;
            z-index: 1;
        }

        .step {
            width: 2.5rem;
            height: 2.5rem;
            border-radius: 50%;
            background: #fff;
            border: 2px solid #dee2e6;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 2;
            transition: all 0.3s ease;
        }

        .step.active {
            border-color: #0d6efd;
            background: #0d6efd;
            color: #fff;
        }

        .step.completed {
            border-color: #198754;
            background: #198754;
            color: #fff;
        }

        .navigation-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
        }
    </style>
</head>
<body class="bg-light">
    <div class="container py-5" x-data="{ 
        currentStep: 1,
        totalSteps: 4,
        nextStep() {
            if (this.currentStep < this.totalSteps) this.currentStep++;
        },
        prevStep() {
            if (this.currentStep > 1) this.currentStep--;
        },
        isStepCompleted(step) {
            return this.currentStep > step;
        }
    }">
        <h1 class="text-center mb-4">Preferències de Viatge</h1>

        <div class="step-indicator mb-4">
            <template x-for="step in totalSteps">
                <div class="step" 
                    :class="{
                        'active': currentStep === step,
                        'completed': isStepCompleted(step)
                    }" 
                    x-text="step"></div>
            </template>
        </div>

        <form method="POST" class="needs-validation" novalidate>
            <div x-show="currentStep === 1" class="card mb-4">
                <div class="card-header bg-warning text-white">
                    <h5 class="mb-0"><i class="bi bi-sort-numeric-down me-2"></i>Prioritats del Viatge</h5>
                </div>
                <div class="card-body">
                    <div class="row g-3">
                        <div class="col-12">
                            <label class="form-label">Ordena per importància (arrossega les opcions):</label>
                            <div id="prioritats-list" class="list-group">
                                <div class="priority-item list-group-item" draggable="true" data-id="pressupost" data-description="Evitar opcions cares, vols barats, menjar econòmic">Pressupost / Diners</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="durada" data-description="Viatges curts vs llargs">Durada del viatge / Temps disponible</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="relax" data-description="Descans, platges, spa, llocs tranquils">Relax & Chill</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="diversio" data-description="Bars, festes, ambient jove">Diversió / Vida nocturna</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="natura" data-description="Muntanyes, parcs, platges verges">Natura i paisatge</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="cultura" data-description="Museus, monuments, llocs històrics">Cultura i història</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="gastronomia" data-description="Bon menjar, cuina local, tastets">Gastronomia</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="aventura" data-description="Senderisme, esports extrems, explorar">Aventura i activitats</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="accessibilitat" data-description="Vols directes, fàcil d'arribar des de la seva ubicació">Accessibilitat</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="sostenibilitat" data-description="Transport ecològic, allotjaments verds">Sostenibilitat (Green Travel)</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="clima" data-description="Prioritzar bon temps segons època de l'any">Clima agradable</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="esdeveniments" data-description="Concerts, festivals, partits, exposicions">Esdeveniments especials</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="shopping" data-description="Mercats, botigues, moda">Compres / Shopping</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="allotjament" data-description="Qualitat, ubicació, comoditat de dormir">Allotjament còmode</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="originalitat" data-description="Visitar llocs nous, no repetits, no turístics">Originalitat / Novetat</div>
                                <div class="priority-item list-group-item" draggable="true" data-id="seguretat" data-description="Països estables, baixos riscos">Seguretat i tranquil·litat</div>
                            </div>
                            <input type="hidden" name="prioritats_ordre" id="prioritats_ordre">
                        </div>
                    </div>
                </div>
            </div>

            <div x-show="currentStep === 2" class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0"><i class="bi bi-heart-fill me-2"></i>Preferències Personals</h5>
                </div>
                <div class="card-body">
                    <div class="row g-3">
                        <div class="col-12">
                            <label class="form-label">Interessos principals de viatge:</label>
                            <div class="row g-2">
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="interessos[]" value="Cultura" class="form-check-input" id="cultura">
                                        <label class="form-check-label" for="cultura">Cultura i Història</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="interessos[]" value="Natura" class="form-check-input" id="natura">
                                        <label class="form-check-label" for="natura">Natura/Aventura</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="interessos[]" value="Platja" class="form-check-input" id="platja">
                                        <label class="form-check-label" for="platja">Platja/Relax</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="interessos[]" value="Esdeveniments" class="form-check-input" id="esdeveniments">
                                        <label class="form-check-label" for="esdeveniments">Esdeveniments</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="interessos[]" value="Gastronomia" class="form-check-input" id="gastronomia">
                                        <label class="form-check-label" for="gastronomia">Gastronomia</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="interessos[]" value="Vida nocturna" class="form-check-input" id="vidanocturna">
                                        <label class="form-check-label" for="vidanocturna">Vida nocturna</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="interessos[]" value="Shopping" class="form-check-input" id="shopping">
                                        <label class="form-check-label" for="shopping">Compres</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="interessos[]" value="Fotografia" class="form-check-input" id="fotografia">
                                        <label class="form-check-label" for="fotografia">Fotografia</label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-4">
                            <label class="form-label">Clima preferit:</label>
                            <select name="clima" class="form-select">
                                <option value="">Selecciona una opció</option>
                                <option value="Calor">Càlid / Estiu</option>
                                <option value="Fred">Fred / Hivern</option>
                                <option value="Temprat">Temprat / Primavera o Tardor</option>
                                <option value="Cap">Cap en especial</option>
                            </select>
                        </div>

                        <div class="col-md-4">
                            <label class="form-label">Importància del viatge ecològic:</label>
                            <select name="green_travel" class="form-select">
                                <option value="">Selecciona una opció</option>
                                <option value="Alta">Alta prioritat</option>
                                <option value="Mitjana">M'interessa</option>
                                <option value="Baixa">No és important</option>
                            </select>
                        </div>

                        <div class="col-md-4">
                            <label class="form-label">Tipus d'allotjament preferit:</label>
                            <select name="allotjament" class="form-select">
                                <option value="">Selecciona una opció</option>
                                <option value="Hotel">Hotel</option>
                                <option value="Hostal">Hostal</option>
                                <option value="Airbnb">Airbnb</option>
                                <option value="Camping">Càmping</option>
                                <option value="Indiferent">Indiferent</option>
                            </select>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label">Nivell d'activitat física:</label>
                            <select name="activitat_fisica" class="form-select">
                                <option value="">Selecciona una opció</option>
                                <option value="Baix">Baix - Passejos suaus</option>
                                <option value="Moderat">Moderat - Caminades llargues</option>
                                <option value="Alt">Alt - Senderisme/Esports</option>
                                <option value="Extrem">Extrem - Aventures intenses</option>
                            </select>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label">Preferència de transport:</label>
                            <select name="transport" class="form-select">
                                <option value="">Selecciona una opció</option>
                                <option value="Transport_public">Transport públic</option>
                                <option value="Cotxe_lloguer">Cotxe de lloguer</option>
                                <option value="Bicicleta">Bicicleta</option>
                                <option value="Combinat">Combinació de mitjans</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <div x-show="currentStep === 3" class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0"><i class="bi bi-info-circle-fill me-2"></i>Informació Bàsica</h5>
                </div>
                <div class="card-body">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Ubicació actual (Ciutat i país):</label>
                            <input type="text" name="ubicacio" class="form-control" required>
                            <div class="invalid-feedback">Si us plau, indica la teva ubicació actual.</div>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Nacionalitat:</label>
                            <input type="text" name="nacionalitat" class="form-control" required>
                            <div class="invalid-feedback">Si us plau, indica la teva nacionalitat.</div>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Data d'inici:</label>
                            <input type="date" name="data_inici" class="form-control">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Data de fi:</label>
                            <input type="date" name="data_fi" class="form-control">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Pressupost màxim (€):</label>
                            <input type="number" name="pressupost" class="form-control" min="0" step="100">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Durada preferida del viatge (dies):</label>
                            <input type="number" name="durada" class="form-control" min="1" max="365">
                        </div>
                    </div>
                </div>
            </div>

            <div x-show="currentStep === 4" class="card mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="bi bi-shield-fill-check me-2"></i>Informació Addicional</h5>
                </div>
                <div class="card-body">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Idiomes que parles:</label>
                            <input type="text" name="idiomes" class="form-control" placeholder="Català, Castellà, Anglès...">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Experiència en viatges:</label>
                            <select name="experiencia" class="form-select">
                                <option value="">Selecciona una opció</option>
                                <option value="Principiant">Principiant - Primers viatges</option>
                                <option value="Intermedi">Intermedi - Alguns viatges</option>
                                <option value="Expert">Expert - Viatger freqüent</option>
                            </select>
                        </div>
                        <div class="col-12">
                            <label class="form-label">Restriccions alimentàries:</label>
                            <div class="row g-2">
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="restriccions_alimentaries[]" value="Vegetaria" class="form-check-input" id="vegetaria">
                                        <label class="form-check-label" for="vegetaria">Vegetarià</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="restriccions_alimentaries[]" value="Vega" class="form-check-input" id="vega">
                                        <label class="form-check-label" for="vega">Vegà</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="restriccions_alimentaries[]" value="Gluten" class="form-check-input" id="gluten">
                                        <label class="form-check-label" for="gluten">Sense gluten</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input type="checkbox" name="restriccions_alimentaries[]" value="Lactosa" class="form-check-input" id="lactosa">
                                        <label class="form-check-label" for="lactosa">Sense lactosa</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-12">
                            <label class="form-label">Restriccions personals o mèdiques:</label>
                            <textarea name="restriccions" class="form-control" rows="3" placeholder="Descriu qualsevol restricció mèdica, mobilitat reduïda, etc."></textarea>
                        </div>
                        <div class="col-12">
                            <label class="form-label">Destinacions a evitar:</label>
                            <textarea name="evitar" class="form-control" rows="2" placeholder="Països o regions que prefereixes no visitar"></textarea>
                        </div>
                        <div class="col-12">
                            <label class="form-label">Comentaris addicionals:</label>
                            <textarea name="comentaris" class="form-control" rows="3" placeholder="Qualsevol altra informació que consideris rellevant"></textarea>
                        </div>
                    </div>
                </div>
            </div>

            <div class="navigation-buttons">
                <button type="button" class="btn btn-secondary" @click="prevStep()" x-show="currentStep > 1">
                    <i class="bi bi-arrow-left me-2"></i>Anterior
                </button>
                <button type="button" class="btn btn-primary" @click="nextStep()" x-show="currentStep < totalSteps">
                    Següent<i class="bi bi-arrow-right ms-2"></i>
                </button>
                <button type="submit" class="btn btn-success" x-show="currentStep === totalSteps">
                    <i class="bi bi-check-circle me-2"></i>Enviar
                </button>
            </div>
            </div>
        </form>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="js/sortable-priorities.js"></script>
    <script>
        // Validació del formulari
        (() => {
            'use strict'
            const forms = document.querySelectorAll('.needs-validation')
            Array.from(forms).forEach(form => {
                form.addEventListener('submit', event => {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                    form.classList.add('was-validated')
                }, false)
            })
        })()

        // Inicialitzar el sistema d'ordenació de prioritats
        document.addEventListener('DOMContentLoaded', () => {
            const sortable = new SortablePriorities('prioritats-list');
        });
    </script>
</body>
</html>
