/* Javascript for SMOWLCHECKREGISTER*/
function SmowlCheckRegXblock(runtime, element, settings) {
    $(function ($) {
        if (settings.has_settings){
            var resultadoo = $(element).find('#resultadoo')[0];
            resultadoo.style.display = "none";
            resultadoo.submit();
        }
    });
}
