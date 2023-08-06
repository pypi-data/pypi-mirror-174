import http.client


def post_batch_events_google_analytics(
    tracking_id,
    ga_client_id,
    event_action,
    event_category="chatbot",
    event_value=1,
    event_label=None,
    v=1,
    hit_type="event",
):

    conn = http.client.HTTPSConnection("www.google-analytics.com")
    payload = f"v={v}&cid={ga_client_id}&tid={tracking_id}&t={hit_type}&ec={event_category}&ea={event_action}&el={event_label}&ev={event_value}"
    headers = {"Content-Type": "text/plain"}
    conn.request("POST", "/batch", payload, headers)
    return conn.getresponse()



if __name__ == "__main__":
    _v = 1
    # t = hit type
    _t = "event"
    # tid = tracking id
    _tid = "UA-246594206-1"
    # cid = client id
    _cid = "f5cd2498-a0bd-44d2-8023-c40102512e71"
    _cid = "483371018.1666945871"
    # ec = event category
    _ec = "Chatbot"
    # ea = event action
    _ea = "test-event-action"

    _el = "test-event-label"

    _ev = 1
    for i in range(10):
        print(post_batch_events_google_analytics(
            tracking_id=_tid,
            ga_client_id=_cid,
            event_action=_ea,
        ).reason)
