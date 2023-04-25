const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
    paymentMethods.forEach(method => {
    method.addEventListener('change', function() {

        if (this.value === 'bank_transfer') {
            document.querySelector('#bank-transfer-details').style.display = 'block'
        } else {
            document.querySelector('#bank-transfer-details').style.display = 'none';
        }
        
        if (this.value === 'visa') {
            document.querySelector('#visa-details').style.display = 'block';
        } else {
            document.querySelector('#visa-details').style.display = 'none';
        }
        
        paymentMethods.forEach(otherMethod => {
        if (otherMethod !== this) {
            otherMethod.checked = false;
        }
        });
    });
});