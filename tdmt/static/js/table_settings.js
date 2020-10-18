globalTableHead = {
    "processing": true,
    "language": {
        search: "_INPUT_",
        searchPlaceholder: "Поиск..",
        sLengthMenu: "_MENU_",
        processing: "Загрузка.."
    },
    "search": {
        "caseInsensitive": true
    },
    "lengthChange": false,
    "pageLength": 50,
    "columnDefs": [
        {
            targets: '_all',
            defaultContent: '-'
        }
    ],
    "buttons": []
};

exportButtons = {
    "buttons": [
        {
            extend: 'excelHtml5',
            exportOptions: {
                columns: ':visible'
            }
        },
        {
            extend: 'pdfHtml5',
            exportOptions: {
                columns: ':visible'
            }
        },
        {
            extend: 'csvHtml5',
            exportOptions: {
                columns: ':visible'
            }
        },
        {
            text: 'Выбрать колонки',
            extend: 'colvis',
            exportOptions: {
                columns: ':visible'
            }
        },
    ],
}

links_viewEditDelete = {
    "data": "links",
    "sortable": false,
    "searchable": false,
    "render": function (data) {
        return "<div class=\"field is-grouped is-grouped-centered action\">" +
            "<p class=\"control\">" +
            "<a class=\"button is-outlined is-text is-small\"" +
            "href='" + data["view"] + "' title=\"Подробнее\">" +
            "<span class=\"icon is-small\"><i class=\"fas fa-eye\"></i></span>" +
            "</a>" +
            "</p>" +
            "<p class=\"control\">" +
            "<a class=\"button is-outlined is-text is-small\"" +
            "href='" + data["edit"] + "' title=\"Редактировать\">" +
            "<span class=\"icon is-small\"><i class=\"fas fa-edit\"></i></span>" +
            "</a>" +
            "</p>" +
            "<p class=\"control\">" +
            "<a class=\"button is-outlined is-text is-small confirm-delete\"" +
            "href='" + data["delete"] + "' title=\"Удалить\">" +
            "<span class=\"icon is-small\"><i class=\"fas fa-trash\"></i></span>" +
            "</a>" +
            "</p>" +
            "</div>";
    }
};

links_editDelete = {
    "data": "links",
    "sortable": false,
    "searchable": false,
    "render": function (data) {
        return "<div class=\"field is-grouped is-grouped-centered action\">" +
            "<p class=\"control\">" +
            "<a class=\"button is-outlined is-text is-small\"" +
            "href='" + data["edit"] + "' title=\"Редактировать\">" +
            "<span class=\"icon is-small\"><i class=\"fas fa-edit\"></i></span>" +
            "</a>" +
            "</p>" +
            "<p class=\"control\">" +
            "<a class=\"button is-outlined is-text is-small confirm-delete\"" +
            "href='" + data["delete"] + "' title=\"Удалить\">" +
            "<span class=\"icon is-small\"><i class=\"fas fa-trash\"></i></span>" +
            "</a>" +
            "</p>" +
            "</div>";
    }
};