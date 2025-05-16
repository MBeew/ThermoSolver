document.getElementById('formulario').addEventListener('submit', async (e) => {
  e.preventDefault();

  const funcion = document.getElementById('funcion').value.trim();
  const x0 = parseFloat(document.getElementById('x0').value.replace(',', '.'));
  const tolerancia = parseFloat(document.getElementById('tolerancia').value.replace(',', '.'));
  const max_iter = parseInt(document.getElementById('max_iter').value);

  const resultadoDiv = document.getElementById('resultado');
  const imagenDiv = document.getElementById('imagen');
  const iterDiv = document.getElementById('iteraciones');

  // Limpieza inicial
  resultadoDiv.classList.remove('d-none', 'alert-danger', 'alert-success');
  resultadoDiv.innerText = '';
  iterDiv.innerHTML = '';
  imagenDiv.innerHTML = '';

  try {
    const respuesta = await fetch('/calcular', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ funcion, x0, tolerancia, max_iter })
    });

    const datos = await respuesta.json();
    const resultado = datos.resultado;

    if (typeof resultado === 'number') {
      resultadoDiv.classList.add('alert-success');
      resultadoDiv.innerText = `Raíz encontrada: ${resultado.toFixed(6)}\nIteraciones necesarias: ${datos.contador}`;
    } else {
      resultadoDiv.classList.add('alert-danger');
      resultadoDiv.innerText = `Error: ${resultado}`;
      return;
    }

    // Mostrar la imagen
    if (datos.imagen) {
      imagenDiv.innerHTML = `<img src="data:image/png;base64,${datos.imagen}" alt="Gráfica de la función" class="img-fluid border" />`;
    }

    // Mostrar iteraciones
    if (datos.iteraciones && datos.iteraciones.length > 0) {
      let html = '<h5 class="mt-4">Iteraciones:</h5><table class="table table-striped">';
      html += '<thead><tr><th>#</th><th>x</th><th>f(x)</th></tr></thead><tbody>';
      datos.iteraciones.forEach(it => {
        html += `<tr><td>${it.iteracion}</td><td>${it.x.toFixed(6)}</td><td>${it.fx.toFixed(6)}</td></tr>`;
      });
      html += '</tbody></table>';
      iterDiv.innerHTML = html;
    }

  } catch (error) {
    resultadoDiv.classList.add('alert-danger');
    resultadoDiv.innerText = 'Error al procesar la solicitud.';
    console.error(error);
  }
});
