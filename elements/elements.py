from selene.support.shared.jquery_style import s, ss


class Elements:
    def element(self, selector: str) -> s:
        return s(selector)

    def elements(self, selector: str) -> ss:
        return ss(selector)
