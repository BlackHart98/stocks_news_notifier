import logging
import typing as t
import requests

# if left is greater than or equal to the right return True vice versa
# I don't need to be exhaustive
def compare_moments_ago(left_moments_ago: str, right_moments_ago) -> bool:
    ago_ord: t.Dict[str, int] = {
        "minute": 0,
        "minutes": 1,
        "hour": 2,
        "hours": 3,
        "day": 4,
        "days": 5,
        "week": 6,
        "weeks": 7,
        "month": 8,
        "months": 9,
        "year": 10,
        "years": 11,
    }
    if (left_moments_ago == ""): return True
    if (right_moments_ago == ""): return False
    left: t.List[str] = left_moments_ago.split(" ")
    right: t.List[str] = right_moments_ago.split(" ")
    if (left[-1] == "ago" and right[-1] == "ago"):
        if ago_ord[left[1]] == ago_ord[right[1]]:
            if (int(left[0]) >= int(right[0])): 
                return True
            else:
                return False
        elif ago_ord[left[1]] >= ago_ord[right[1]]:
            return True
        else:
            return False
    elif (left[-1] == "ago"):
        return False
    else:
        return True
    


def check_updates(previous_state: t.Optional[t.Dict[str, t.Any]], current_state: t.Optional[t.Dict[str, t.Any]]) -> t.Optional[t.Dict[str, t.Any]]:
    previous_news = previous_state["news"] if previous_state is not None else []
    if current_state is None:
        return None
    else:
        
        logging.info(f"Previous state: {previous_state}\nCurrent state {current_state}")
        
        result = {"tick" : current_state["tick"], "news" : []}
        current_dict : t.Dict[str, t.Any] = {}
        previous_dict : t.Dict[str, t.Any] = {}
        for item in current_state["news"]:
            current_dict[item["article_link"]] = item
        for item in previous_news:
            previous_dict[item["article_link"]] = item
        
        logging.info(f"Current dict: {current_dict}\nPrevious dict {previous_dict}")
        
        for item in current_dict:
            if item not in previous_dict:
                result["news"] += [current_dict[item]]
        
        if len(result["news"]) == 0:
            return None
        else: 
            return result


        
# Naive approach selenium grid session management 
def purge_all_selenium_sessions(url: str, session_ids: t.List[str]) -> None:
    for item in session_ids:
        # if is_url_alive(f"{url}/session/{item}"):
            logging.info(f"Destroy session: {item}")
            requests.delete(f"{url}/session/{item}")


def get_link_content_association(site_query: t.Optional[t.Dict[str, t.Any]]) -> t.Dict[str, t.Any]:
    if site_query is None: return {}
    result : t.Dict[str, t.Any] = {}
    for item in site_query["news"]:
        result[item["article_link"]] = item["article_content"]
    return result
