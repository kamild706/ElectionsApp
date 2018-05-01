$('.choice').each(function () {
    let checkbox = $(this).find($('input'));
    let isChecked = checkbox.is(':checked');

    $(this).css('background-color', isChecked ? '#e9ecef' : 'inherit');
});

$('.choice').click(function () {
    let checkbox = $(this).find($('input'));
    let isChecked = checkbox.is(':checked');

    $(this).css('background-color', !isChecked ? '#e9ecef' : 'inherit');
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

    if (selectedCandidates > maxVotes) {
        alert("Wybrales zbyt wielu kandydatow");
        return false;
    }
    return true;
}

