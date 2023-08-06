
try {
    new Function("import('/reactfiles/frontend/main.e9f61375.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.e9f61375.js';
    el.type = 'module';
    document.body.appendChild(el);
}
