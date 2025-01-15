document.addEventListener('DOMContentLoaded', function() {
    // Función para cargar datos desde un archivo CSV
    function loadCSV(file, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', file, true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                callback(xhr.responseText);
            }
        };
        xhr.send();
    }

    // Función para procesar datos CSV
    function processCSV(csvText) {
        var lines = csvText.split('\n');
        var result = [];
        var headers = lines[0].split(',');
        for (var i = 1; i < lines.length; i++) {
            var currentline = lines[i].split(',');
            // Saltar filas con valores NaN o vacíos
            if (currentline.includes('NaN') || currentline.includes('')) continue;
            var obj = {};
            for (var j = 0; j < headers.length; j++) {
                obj[headers[j]] = currentline[j];
            }
            result.push(obj);
        }
        return result;
    }

    // Cargar y procesar datos de tops diarios
    loadCSV('/data/tops_diarios.csv', function(responseText) {
        var tops_data = processCSV(responseText);
        var tops_tbody = document.getElementById('tops-semana');
        tops_tbody.innerHTML = ''; // Limpiar contenido previo

        tops_data.forEach(function(item) {
            var row = document.createElement('tr');
            var cell1 = document.createElement('td');
            var cell2 = document.createElement('td');
            cell1.textContent = item.EMISOR;
            cell2.textContent = parseFloat(item.VARIA_DIA).toFixed(2) + '%';
            cell2.style.color = 'green'; // Colorear en verde para positivos
            row.appendChild(cell1);
            row.appendChild(cell2);
            tops_tbody.appendChild(row);
        });
    });

    // Cargar y procesar datos de flops diarios
    loadCSV('/data/flops_diarios.csv', function(responseText) {
        var flops_data = processCSV(responseText);
        var flops_tbody = document.getElementById('flops-semana');
        flops_tbody.innerHTML = ''; // Limpiar contenido previo

        flops_data.forEach(function(item) {
            var row = document.createElement('tr');
            var cell1 = document.createElement('td');
            var cell2 = document.createElement('td');
            cell1.textContent = item.EMISOR;
            cell2.textContent = parseFloat(item.VARIA_DIA).toFixed(2) + '%';
            cell2.style.color = 'red'; // Colorear en rojo para negativos
            row.appendChild(cell1);
            row.appendChild(cell2);
            flops_tbody.appendChild(row);
        });
    });
});
