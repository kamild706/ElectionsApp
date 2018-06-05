/* global $ */
let color = "#cacdd1";

$('.choice').each(function () {
    let checkbox = $(this).find($('input'));
    let isChecked = checkbox.is(':checked');

    $(this).css('background-color', isChecked ? color : 'inherit');
});

$('.choice').click(function () {
    let checkbox = $(this).find($('input'));
    let isChecked = checkbox.is(':checked');

    $(this).css('background-color', !isChecked ? color : 'inherit');
    checkbox.prop('checked', !isChecked);
});

function validateForm() {
    let maxVotes = Number($("#maxVotes").text());
    let selectedCandidates = 0;

    $('.choice').each(function () {
        let checkbox = $(this).find($('input'));
        if (checkbox.is(':checked'))
            selectedCandidates++;
    });

    if (selectedCandidates === 0) {
        alert("Musisz wybrać conajmniej 1 pozycję");
        return false;
    }

    if (selectedCandidates > maxVotes) {
        alert("Wybrales zbyt wiele odpowiedzi");
        return false;
    }
    return true;
}

