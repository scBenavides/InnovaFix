document.getElementById('busquedaCliente').addEventListener('keyup', function() {
  var filtro = this.value.toLowerCase();
  document.querySelectorAll('table tbody tr').forEach(function(row) {
    row.style.display = row.textContent.toLowerCase().includes(filtro) ? '' : 'none';
  });
});