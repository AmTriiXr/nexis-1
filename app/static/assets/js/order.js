window.onload = function() {
    const productSort = document.getElementById('product-sort');
    productSort.onchange = function() {
        const sortOption = productSort.value;
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('ordering', sortOption);
        window.location.href = currentUrl.href;
    }
}