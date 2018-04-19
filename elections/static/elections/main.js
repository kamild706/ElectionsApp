$(function() {
    $('.choice').click(function() {
        let id = $(this).find($('input')).attr('id');
        let isChecked = toggleCheckboxState(id);
        $(this).css('background-color', isChecked ? '#e9ecef' : 'inherit');
    });
});

function toggleCheckboxState(id) {
    let isChecked = $('#' + id).is(':checked');
    $('#' + id).prop('checked', isChecked ? false : true);
    return !isChecked;
}