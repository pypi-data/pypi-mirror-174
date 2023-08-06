from encord_active_app.common.components import sticky_header
from encord_active_app.common.utils import setup_page
from encord_active_app.data_quality.common import IndexType, load_available_indices
from encord_active_app.data_quality.sub_pages.explorer import ExplorerPage
from encord_active_app.data_quality.sub_pages.summary import SummaryPage


def summary(index_type: IndexType):
    def render():
        setup_page()
        page = SummaryPage()

        with sticky_header():
            page.sidebar_options()

        page.build(index_type.value)

    return render


def explorer(index_type: IndexType):
    def render():
        setup_page()
        page = ExplorerPage()
        available_indices = load_available_indices(index_type.value)

        with sticky_header():
            selected_df = page.sidebar_options(available_indices)

        if selected_df is None:
            return

        page.build(selected_df)

    return render
