var inputs = document.querySelectorAll('input[type="password"]');
inputs[0].classList.add("form-control");
inputs[1].classList.add("form-control");

inputs[0].setAttribute('placeholder', 'New Password');
inputs[1].setAttribute('placeholder', 'Confirm Password');

var labels = document.querySelectorAll('label');
labels[0].remove();
labels[1].remove();

var listItems = document.querySelectorAll('li');
listItems[11].remove();
listItems[12].remove();
listItems[13].remove();
listItems[14].remove();