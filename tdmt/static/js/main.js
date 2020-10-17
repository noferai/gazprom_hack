function filter_table(_label, _value) {
    dataTable
        .columns()
        .header()
        .each(function (value, index) {
            if (value.textContent.toLowerCase() === _label.toLowerCase()) {
                dataTable.column(index).search(_value).draw();
            }
        });
}

function format_comment(d) {
    return '<table class="sub-row">' +
        '<tr>' +
        '<td class="has-text-weight-bold">Комментарий: </td>' +
        '<td>' + d.comment + '</td>' +
        '</tr>' +
        '</table>';
}


postForm = function (form, button) {
    var formData = new FormData(form);
    if (button) {
        formData.append(button.name, button.value);
    } else {
        if (form.id) {
            document.querySelectorAll('select[form=' + form.id + ']').forEach(($select) => {
                formData.append($select.name, $select.value);
            });
        }
    }
    fetch(document.location.href, {
        method: 'POST',
        headers: {
            'X-Fetch': 'true'
        },
        body: formData
    }).then(function (data) {
        return data.json();
    }).then(function (jsonResponse) {
        Turbolinks.visit(jsonResponse.url, {
            action: "replace"
        });
    }).catch(function (error) {
        console.log('request failed', error);
    })
};

Turbolinks.setProgressBarDelay(50);


function ready(fn) {
    if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading") {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

ready(function () {
    var elementList = document.querySelectorAll('a.launch-modal');
    Array.prototype.forEach.call(elementList, function (el, i) {
        el.addEventListener('click', function (event) {
            event.preventDefault();

            var modalFormTitle = document.querySelector('#modal-form .modal-card-title');
            modalFormTitle.innerHTML = event.target.textContent;

            var modalForm = document.querySelector('#modal-form');
            modalForm.querySelector('iframe').setAttribute('src', event.target.parentNode.getAttribute('href'));
            modalForm.classList.add('is-clipped');
            modalForm.classList.add('is-active');
        });
    });

    document.querySelectorAll('form').forEach(($form) => {
        if (!$form.hasAttribute('data-nofetch')) {
            $form.addEventListener('submit', function (event) {
                event.preventDefault();
                if ($form.method.toLowerCase() == 'get') {
                    Turbolinks.visit(document.location.pathname + "?q=" + encodeURIComponent(document.querySelector('#id_q').value));
                } else {
                    postForm($form);
                }
            });
        }
    });

    $('.select select').select2({
        placeholder: "Выберите значение",
        minimumResultsForSearch: 7,
        allowClear: false,
        width: "element",
    });

    $('.select select.allowclear').select2({
        placeholder: "Выберите значение",
        minimumResultsForSearch: 7,
        allowClear: true,
        width: "element"
    });

    $('div.control.search-table label').append('<span class="icon is-small is-left"><i class="fa fa-search"></i></span>');

    $('a.filter').click(function (e) {
        e.preventDefault();
        $('div.filters-toggle').toggle("slow");
    });

    $('a.report').click(function (e) {
        e.preventDefault();
        $('div.dt-buttons').toggle("slow");
    });

    $('.close-modal').click(function (e) {
        e.preventDefault();
        $('#confirm-delete-modal').removeClass("is-active");
    });

    $('body').on('click', '.confirm-delete', function (e) {
        e.preventDefault();
        let target = e.currentTarget.attributes.href.nodeValue;
        $('#confirm-delete-modal').addClass("is-active").promise().done(function () {
            $(this).find('a.confirm').attr('href', target);
        });
    });

    $('#tasks tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = dataTable.row(tr);

        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
        } else {
            row.child(format_comment(row.data()), "is-paddingless").show();
            tr.addClass('shown');
        }
    });
});