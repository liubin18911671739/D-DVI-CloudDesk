
function socketio_on () {
    socket.on('storage_nodes', function (data) {
        var data = JSON.parse(data)
        dtUpdateInsert(
            table,
            {...table.row("#"+data.id).data(),...data},
            false
        )
    })
}
$(document).ready(function () {
    $('.admin-status').show()
    table = $('#storage_nodes').DataTable({
        "ajax": {
            "url": "/admin/table/storage_node",
            "dataSrc": ""
        },
        "language": {
            "loadingRecords": '<i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i><span class="sr-only">Loading...</span>'
        },
        "rowId": "id",
        "columns": [
            {
                "data": "status",
                "defaultContent": ""
            },
            {
                "data": "status_time",
                "render": (data) => {
                    return moment.unix(data).fromNow();
                }
            },
            {
                "data": "id"
            },
            {
                "data": "storage_pools",
            },
            {
                "data": "verify_cert"
            },
        ],
        "columnDefs": [
            {
                "targets": 4,
                "render": function ( data, type, full, meta ) {
                    if( full.status == "deleted"){
                        return ""
                    }
                    if( full.id.includes("isard-storage") ){
                        return "Doesn't apply"
                    }
                    if(data){
                        return '<i class="fa fa-circle" aria-hidden="true" style="color:green"></i>'
                    }else{
                        return '<i class="fa fa-exclamation-triangle" style="color:lightred" title="STORAGE_DOMAIN for this host is not a valid DNS. You should be using a reliable network."></i>'
                    }
                }},
        ],
    })
    $.getScript("/isard-admin/static/admin/js/socketio.js", socketio_on)
})
