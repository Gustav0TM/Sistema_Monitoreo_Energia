document.addEventListener('DOMContentLoaded', () => {
    let chart;
    let intervalo;
    let historialData = { labels: [], datasets: [] }; // historial global para mantener los datos

    const ctx = document.getElementById('graficoCanvas').getContext('2d');
    const tipoGraficoSelect = document.getElementById('tipo-grafico');
    const disp1Select = document.getElementById('dispositivo1');
    const disp2Select = document.getElementById('dispositivo2');

    const colores = {
        Tuya1: 'rgba(54, 162, 235, 0.7)',
        Tuya2: 'rgba(255, 99, 132, 0.7)',
        Tuya3: 'rgba(255, 206, 86, 0.7)',
        Tuya4: 'rgba(75, 192, 192, 0.7)',
        Tuya5: 'rgba(153, 102, 255, 0.7)'
    };

    // 🔹 Cargar dispositivos únicos
    function cargarDispositivos() {
        fetch('/api/lecturas')
            .then(res => res.json())
            .then(data => {
                const nombres = [...new Set(data.map(d => d.nombre))];
                disp1Select.innerHTML = '';
                disp2Select.innerHTML = '';
                nombres.forEach(nombre => {
                    const opt1 = document.createElement('option');
                    const opt2 = document.createElement('option');
                    opt1.value = nombre;
                    opt2.value = nombre;
                    opt1.textContent = nombre;
                    opt2.textContent = nombre;
                    disp1Select.appendChild(opt1);
                    disp2Select.appendChild(opt2);
                });
                disp1Select.value = nombres[0];
                disp2Select.value = nombres[1] || nombres[0];
            })
            .catch(err => console.error('❌ Error al cargar dispositivos:', err));
    }

    // 🔹 Obtener datos desde la API
    function obtenerDatos() {
        const tipo = tipoGraficoSelect.value;
        const url = (tipo === 'historial') ? '/api/lecturas?limit=10' : '/api/simular';
        return fetch(url).then(res => res.json());
    }

    // 🔹 Inicializar historial con las últimas 10 lecturas
    async function inicializarHistorial() {
        const data = await obtenerDatos();
        const dispositivos = [...new Set(data.map(d => d.nombre))];

        historialData.labels = [];
        historialData.datasets = dispositivos.map(nombre => ({
            label: nombre,
            data: [],
            borderColor: colores[nombre].replace('0.7', '1'),
            backgroundColor: colores[nombre],
            tension: 0.3
        }));

        // Rellenar las 10 últimas lecturas por dispositivo
        dispositivos.forEach(nombre => {
            const lecturasDisp = data.filter(d => d.nombre === nombre).slice(-10);
            lecturasDisp.forEach(lectura => {
                if (!historialData.labels.includes(lectura.hora)) {
                    historialData.labels.push(lectura.hora);
                }
                const ds = historialData.datasets.find(ds => ds.label === nombre);
                ds.data.push(lectura.potencia);
                if (ds.data.length > 10) ds.data.shift();
            });
        });
    }

    // 🔹 Actualizar gráfico
    async function actualizarGrafico() {
        const tipo = tipoGraficoSelect.value;
        const data = await obtenerDatos();

        if (tipo === 'barras') {
            if (chart) chart.destroy();

            const d1 = data.find(d => d.nombre === disp1Select.value);
            const d2 = data.find(d => d.nombre === disp2Select.value);
            if (!d1 || !d2) return;

            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Voltaje (V)', 'Corriente (A)', 'Potencia (W)', 'Frecuencia (Hz)'],
                    datasets: [
                        {
                            label: d1.nombre,
                            data: [d1.voltaje, d1.corriente, d1.potencia, d1.frecuencia],
                            backgroundColor: colores[d1.nombre],
                            borderColor: colores[d1.nombre].replace('0.7', '1'),
                            borderWidth: 1
                        },
                        {
                            label: d2.nombre,
                            data: [d2.voltaje, d2.corriente, d2.potencia, d2.frecuencia],
                            backgroundColor: colores[d2.nombre],
                            borderColor: colores[d2.nombre].replace('0.7', '1'),
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: { display: true, text: 'Comparativa de Consumo (Tiempo Real)' },
                        legend: { position: 'top' }
                    },
                    scales: { y: { beginAtZero: true } }
                }
            });

        } else if (tipo === 'pastel') {
            if (chart) chart.destroy();

            const labels = data.map(d => d.nombre);
            const potencias = data.map(d => d.potencia);
            const coloresBG = labels.map(n => colores[n]);

            chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels,
                    datasets: [{
                        data: potencias,
                        backgroundColor: coloresBG,
                        borderColor: coloresBG.map(c => c.replace('0.7', '1')),
                        borderWidth: 1
                    }]
                },
                options: {
                    plugins: {
                        title: { display: true, text: 'Porcentaje de Consumo por Dispositivo' },
                        legend: { position: 'right' }
                    }
                }
            });

        } else if (tipo === 'historial') {
            // Crear gráfico si no existe
            if (!chart || chart.config.type !== 'line') {
                await inicializarHistorial();
                chart = new Chart(ctx, {
                    type: 'line',
                    data: historialData,
                    options: {
                        responsive: true,
                        plugins: {
                            title: { display: true, text: 'Historial de Potencia (Últimas 10 Lecturas)' },
                            legend: { position: 'bottom' }
                        },
                        scales: {
                            y: { beginAtZero: true, title: { display: true, text: 'Potencia (W)' } },
                            x: { title: { display: true, text: 'Hora de Lectura' } }
                        },
                        animation: false
                    }
                });
            } else {
                // Agregar nueva lectura en tiempo real
                const dispositivos = [...new Set(data.map(d => d.nombre))];
                const ultimaLectura = data[data.length - 1];
                if (!ultimaLectura) return;

                const nuevaEtiqueta = ultimaLectura.hora || new Date().toLocaleTimeString();
                if (!historialData.labels.includes(nuevaEtiqueta)) {
                    historialData.labels.push(nuevaEtiqueta);
                    if (historialData.labels.length > 10) historialData.labels.shift();
                }

                dispositivos.forEach(nombre => {
                    const ds = historialData.datasets.find(ds => ds.label === nombre);
                    const lecturas = data.filter(d => d.nombre === nombre);
                    const ultima = lecturas[lecturas.length - 1];
                    if (ds) {
                        ds.data.push(ultima ? ultima.potencia : 0);
                        if (ds.data.length > 10) ds.data.shift();
                    }
                });

                chart.update();
            }
        }
    }

    // 🔁 Refresco automático cada 2 segundos
    function iniciarAutoRefresh() {
        if (intervalo) clearInterval(intervalo);
        intervalo = setInterval(actualizarGrafico, 2000);
    }

    // 🎯 Inicialización
    cargarDispositivos();
    tipoGraficoSelect.addEventListener('change', () => {
        if (chart) chart.destroy();
        chart = null;
        actualizarGrafico();
        iniciarAutoRefresh();
    });
    disp1Select.addEventListener('change', actualizarGrafico);
    disp2Select.addEventListener('change', actualizarGrafico);

    actualizarGrafico();
    iniciarAutoRefresh();
});
