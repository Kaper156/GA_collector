# TODO test this
class GoogleAuthPage:
    login_entry = 'input#identifierId'


class GAPage:
    btn_export = '.ID-exportControlButton'
    choice_to_csv = 'li.ACTION-export.TARGET-CSV'
    btn_sort = 'th.ACTION-sort'
    btn_next_page = 'li.ACTION-paginate:nth-of-type(2)'
    pagination_nums = 'span.C_PAGINATION_ROWS_LONG>label'

    anchor_loaded = btn_sort
    anchor_nex_page = btn_next_page
    main_frame = 'iframe#galaxyIframe'
    main_frame_ID = 'galaxyIframe'
    alert_loading_ID = 'ID-reportLoading'
    alert_download_ID = 'ID-messageBox'
