# server.py
from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict, List, Optional, Any
import json
import requests
import sys

    

# --- Constants ---
FB_API_VERSION = "v22.0"
FB_GRAPH_URL = f"https://graph.facebook.com/{FB_API_VERSION}"
DEFAULT_AD_ACCOUNT_FIELDS = [
    'name', 'business_name', 'age', 'account_status', 'balance',
    'amount_spent', 'attribution_spec', 'account_id', 'business',
    'business_city', 'brand_safety_content_filter_levels', 'currency',
    'created_time', 'id'
]

# Create an MCP server
mcp = FastMCP("fb-api-mcp-server")

# Add a global variable to store the token
FB_ACCESS_TOKEN = None

# --- Helper Functions ---

def _get_fb_access_token() -> str:
    """
    Get Facebook access token from command line arguments.
    Caches the token in memory after first read.

    Returns:
        str: The Facebook access token.

    Raises:
        Exception: If no token is provided in command line arguments.
    """
    global FB_ACCESS_TOKEN
    if FB_ACCESS_TOKEN is None:
        # Look for --fb-token argument
        if "--fb-token" in sys.argv:
            token_index = sys.argv.index("--fb-token") + 1
            if token_index < len(sys.argv):
                FB_ACCESS_TOKEN = sys.argv[token_index]
                print(f"Using Facebook token from command line arguments")
            else:
                raise Exception("--fb-token argument provided but no token value followed it")
        else:
            raise Exception("Facebook token must be provided via '--fb-token' command line argument")

    return FB_ACCESS_TOKEN

def _make_graph_api_call(url: str, params: Dict[str, Any]) -> Dict:
    """Makes a GET request to the Facebook Graph API and handles the response."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        # Log the error and re-raise or handle more gracefully
        print(f"Error making Graph API call to {url} with params {params}: {e}")
        # Depending on desired behavior, you might want to raise a custom exception
        # or return a specific error structure. Re-raising keeps the current behavior.
        raise


def _prepare_params(base_params: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Adds optional parameters to a dictionary if they are not None. Handles JSON encoding."""
    params = base_params.copy()
    for key, value in kwargs.items():
        if value is not None:
            # Parameters that need JSON encoding
            if key in ['filtering', 'time_range', 'time_ranges', 'effective_status', 
                       'special_ad_categories', 'objective', 
                       'buyer_guarantee_agreement_status'] and isinstance(value, (list, dict)):
                params[key] = json.dumps(value)
            elif key == 'fields' and isinstance(value, list):
                 params[key] = ','.join(value)
            elif key == 'action_attribution_windows' and isinstance(value, list):
                 params[key] = ','.join(value)
            elif key == 'action_breakdowns' and isinstance(value, list):
                 params[key] = ','.join(value)
            elif key == 'breakdowns' and isinstance(value, list):
                 params[key] = ','.join(value)
            else:
                params[key] = value
    return params


def _fetch_node(node_id: str, **kwargs) -> Dict:
    """Helper to fetch a single object (node) by its ID."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{node_id}"
    params = _prepare_params({'access_token': access_token}, **kwargs)
    return _make_graph_api_call(url, params)

def _fetch_edge(parent_id: str, edge_name: str, **kwargs) -> Dict:
    """Helper to fetch a collection (edge) related to a parent object."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{parent_id}/{edge_name}"
    
    # Handle time parameters specifically for activities edge if needed
    time_params = {}
    if edge_name == 'activities':
        time_range = kwargs.pop('time_range', None)
        since = kwargs.pop('since', None)
        until = kwargs.pop('until', None)
        if time_range:
            time_params['time_range'] = time_range
        else:
            if since: time_params['since'] = since
            if until: time_params['until'] = until
            
    base_params = {'access_token': access_token}
    params = _prepare_params(base_params, **kwargs)
    params.update(_prepare_params({}, **time_params)) # Add specific time params

    return _make_graph_api_call(url, params)


def _make_graph_api_post(url: str, data: Dict[str, Any]) -> Dict:
    """Makes a POST request to the Facebook Graph API for creating/updating objects."""
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making Graph API POST to {url}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                return {"error": error_detail}
            except Exception:
                pass
        raise


def _make_graph_api_delete(url: str, params: Dict[str, Any]) -> Dict:
    """Makes a DELETE request to the Facebook Graph API for archiving/deleting objects."""
    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making Graph API DELETE to {url}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                return {"error": error_detail}
            except Exception:
                pass
        raise


def _make_graph_api_search(search_type: str, params: Dict[str, Any]) -> Dict:
    """Makes a GET request to the Facebook Graph API /search endpoint."""
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/search"
    params['access_token'] = access_token
    params['type'] = search_type
    return _make_graph_api_call(url, params)


def _build_insights_params(
    params: Dict[str, Any],
    fields: Optional[List[str]] = None,
    date_preset: Optional[str] = None,
    time_range: Optional[Dict[str, str]] = None,
    time_ranges: Optional[List[Dict[str, str]]] = None,
    time_increment: Optional[str] = None,
    level: Optional[str] = None,
    action_attribution_windows: Optional[List[str]] = None,
    action_breakdowns: Optional[List[str]] = None,
    action_report_time: Optional[str] = None,
    breakdowns: Optional[List[str]] = None,
    default_summary: bool = False,
    use_account_attribution_setting: bool = False,
    use_unified_attribution_setting: bool = True,
    filtering: Optional[List[dict]] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    offset: Optional[int] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    locale: Optional[str] = None
) -> Dict[str, Any]:
    """Builds the common parameter dictionary for insights API calls."""
    
    # Use the generic parameter builder first
    params = _prepare_params(
        params,
        fields=fields,
        level=level,
        action_attribution_windows=action_attribution_windows,
        action_breakdowns=action_breakdowns,
        action_report_time=action_report_time,
        breakdowns=breakdowns,
        filtering=filtering,
        sort=sort,
        limit=limit,
        after=after,
        before=before,
        offset=offset,
        locale=locale
    )

    # Handle time parameters (specific logic for insights)
    time_params_provided = time_range or time_ranges or since or until
    if not time_params_provided and date_preset:
        params['date_preset'] = date_preset
    if time_range:
        params['time_range'] = json.dumps(time_range)
    if time_ranges:
        params['time_ranges'] = json.dumps(time_ranges)
    if time_increment and time_increment != 'all_days': # API default is all_days
        params['time_increment'] = time_increment
        
    # Time-based pagination (only if specific time range isn't set)
    if not time_range and not time_ranges:
        if since:
            params['since'] = since
        if until:
            params['until'] = until

    # Boolean flags need specific handling ('true'/'false' strings)
    if default_summary:
        params['default_summary'] = 'true'
    if use_account_attribution_setting:
        params['use_account_attribution_setting'] = 'true'
    # Only add unified if True (it defaults to False in API if omitted)
    if use_unified_attribution_setting:
        params['use_unified_attribution_setting'] = 'true'

    return params



# --- MCP Tools ---
@mcp.tool()
def list_ad_accounts() -> Dict:
    """List down the ad accounts and their names associated with your Facebook account.
        CRITICAL: This function MUST automatically fetch ALL pages using pagination. 
        When the response contains a 'paging.next' URL, IMMEDIATELY and AUTOMATICALLY 
        use the facebook_fetch_pagination_url tool to fetch the next page. Continue 
        this process until no 'next' URL exists. Do NOT ask the user for permission 
        to continue pagination. Do NOT stop after the first page. Always return the 
        complete consolidated list of ALL ad accounts across all pages in a single 
        response. This is a requirement, not optional behavior."""
    # This uses a specific endpoint structure not fitting _fetch_node/_fetch_edge easily
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/me"
    params = {
        'access_token': access_token,
        'fields': 'adaccounts{name}' # Specific field structure
    }
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_details_of_ad_account(act_id: str, fields: list[str] = None) -> Dict:
    """Get details of a specific ad account as per the fields provided
    Args:
        act_id: The act ID of the ad account, example: act_1234567890
        fields: The fields to get from the ad account. If None, defaults are used.
                Available fields include: name, business_name, age, account_status,
                balance, amount_spent, attribution_spec, account_id, business,
                business_city, brand_safety_content_filter_levels, currency,
                created_time, id.
    Returns:    
        A dictionary containing the details of the ad account
    """
    effective_fields = fields if fields is not None else DEFAULT_AD_ACCOUNT_FIELDS
    return _fetch_node(node_id=act_id, fields=effective_fields)


# --- Insigbts API Tools ---

@mcp.tool()
def get_adaccount_insights(
    act_id: str,
    fields: Optional[List[str]] = None,
    date_preset: str = 'last_30d',
    time_range: Optional[Dict[str, str]] = None,
    time_ranges: Optional[List[Dict[str, str]]] = None,
    time_increment: str = 'all_days',
    level: str = 'account',
    action_attribution_windows: Optional[List[str]] = None,
    action_breakdowns: Optional[List[str]] = None,
    action_report_time: Optional[str] = None,
    breakdowns: Optional[List[str]] = None,
    default_summary: bool = False,
    use_account_attribution_setting: bool = False,
    use_unified_attribution_setting: bool = True,
    filtering: Optional[List[dict]] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    offset: Optional[int] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    locale: Optional[str] = None
) -> Dict:
    """Retrieves performance insights for a specified Facebook ad account.

    This tool interfaces with the Facebook Graph API's Insights edge to fetch comprehensive
    performance data, such as impressions, reach, cost, conversions, and more. It supports
    various options for filtering, time breakdowns, and attribution settings. Note that
    some metrics returned might be estimated or in development
    CRITICAL: This function MUST automatically fetch ALL pages using pagination. 
    When the response contains a 'paging.next' URL, IMMEDIATELY and AUTOMATICALLY 
    use the facebook_fetch_pagination_url tool to fetch the next page. Continue 
    this process until no 'next' URL exists. Do NOT ask the user for permission 
    to continue pagination. Do NOT stop after the first page. Always return the 
    complete consolidated list of ALL ad accounts across all pages in a single 
    response. This is a requirement, not optional behavior..

    Args:
        act_id (str): The target ad account ID, prefixed with 'act_', e.g., 'act_1234567890'.
        fields (Optional[List[str]]): A list of specific metrics and fields to retrieve.
            If omitted, a default set is returned by the API. Common examples include:
                - 'account_currency', 'account_id', 'account_name'
                - 'actions', 'clicks', 'conversions'
                - 'cpc', 'cpm', 'cpp', 'ctr'
                - 'frequency', 'impressions', 'reach', 'spend'.
        date_preset (str): A predefined relative time range for the report.
            Options: 'today', 'yesterday', 'this_month', 'last_month', 'this_quarter',
            'maximum', 'last_3d', 'last_7d', 'last_14d', 'last_28d', 'last_30d',
            'last_90d', 'last_week_mon_sun', 'last_week_sun_sat', 'last_quarter',
            'last_year', 'this_week_mon_today', 'this_week_sun_today', 'this_year'.
            Default: 'last_30d'. This parameter is ignored if 'time_range', 'time_ranges',
            'since', or 'until' is provided.
        time_range (Optional[Dict[str, str]]): A specific time range defined by 'since' and 'until'
            dates in 'YYYY-MM-DD' format, e.g., {'since': '2023-10-01', 'until': '2023-10-31'}.
            Overrides 'date_preset'. Ignored if 'time_ranges' is provided.
        time_ranges (Optional[List[Dict[str, str]]]): An array of time range objects
            ({'since': '...', 'until': '...'}) for comparing multiple periods. Overrides
            'time_range' and 'date_preset'. Time ranges can overlap.
        time_increment (str | int): Specifies the granularity of the time breakdown.
            - An integer from 1 to 90 indicates the number of days per data point.
            - 'monthly': Aggregates data by month.
            - 'all_days': Provides a single summary row for the entire period.
            Default: 'all_days'.
        level (str): The level of aggregation for the insights.
            Options: 'account', 'campaign', 'adset', 'ad'.
            Default: 'account'.
        action_attribution_windows (Optional[List[str]]): Specifies the attribution windows
            to consider for actions (conversions). Examples: '1d_view', '7d_view',
            '28d_view', '1d_click', '7d_click', '28d_click', 'dda', 'default'.
            The API default may vary; ['7d_click', '1d_view'] is common.
        action_breakdowns (Optional[List[str]]): Segments the 'actions' results based on
            specific dimensions. Examples: 'action_device', 'action_type',
            'conversion_destination', 'action_destination'. Default: ['action_type'].
        action_report_time (Optional[str]): Determines when actions are counted.
            - 'impression': Actions are attributed to the time of the ad impression.
            - 'conversion': Actions are attributed to the time the conversion occurred.
            - 'mixed': Uses 'impression' time for paid metrics, 'conversion' time for organic.
            Default: 'mixed'.
        breakdowns (Optional[List[str]]): Segments the results by dimensions like demographics
            or placement. Examples: 'age', 'gender', 'country', 'region', 'dma',
            'impression_device', 'publisher_platform', 'platform_position', 'device_platform'.
            Note: Not all breakdowns can be combined.
        default_summary (bool): If True, includes an additional summary row in the response.
            Default: False.
        use_account_attribution_setting (bool): If True, forces the report to use the
            attribution settings defined at the ad account level. Default: False.
        use_unified_attribution_setting (bool): If True, uses the unified attribution
            settings defined at the ad set level. This is generally recommended for
            consistency with Ads Manager reporting. Default: True.
        filtering (Optional[List[dict]]): A list of filter objects to apply to the data.
            Each object should have 'field', 'operator', and 'value' keys.
            Example: [{'field': 'spend', 'operator': 'GREATER_THAN', 'value': 50}].
        sort (Optional[str]): Specifies the field and direction for sorting the results.
            Format: '{field_name}_ascending' or '{field_name}_descending'.
            Example: 'impressions_descending'.
        limit (Optional[int]): The maximum number of results to return in one API response page.
        after (Optional[str]): A pagination cursor pointing to the next page of results.
            Obtained from the 'paging.cursors.after' field of a previous response.
        before (Optional[str]): A pagination cursor pointing to the previous page of results.
            Obtained from the 'paging.cursors.before' field of a previous response.
        offset (Optional[int]): An alternative pagination method; skips the specified
            number of results. Use cursor-based pagination ('after'/'before') when possible.
        since (Optional[str]): For time-based pagination (used if 'time_range' and 'time_ranges'
            are not set), the start timestamp (Unix or strtotime value).
        until (Optional[str]): For time-based pagination (used if 'time_range' and 'time_ranges'
            are not set), the end timestamp (Unix or strtotime value).
        locale (Optional[str]): The locale for text responses (e.g., 'en_US'). This controls 
            language and formatting of text fields in the response.

    Returns:
        Dict: A dictionary containing the requested ad account insights. The main results
              are in the 'data' list, and pagination info is in the 'paging' object.

    Example:
        ```python
        # Get basic ad account performance for the last 30 days
        insights = get_adaccount_insights(
            act_id="act_123456789",
            fields=["impressions", "clicks", "spend", "ctr"],
            limit=25
        )

        # Fetch the next page if available using the pagination tool
        next_page_url = insights.get("paging", {}).get("next")
        if next_page_url:
            next_page_results = fetch_pagination_url(url=next_page_url)
            print("Fetched next page results.")
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/insights"
    params = {'access_token': access_token}

    params = _build_insights_params(
        params=params,
        fields=fields,
        date_preset=date_preset,
        time_range=time_range,
        time_ranges=time_ranges,
        time_increment=time_increment,
        level=level,
        action_attribution_windows=action_attribution_windows,
        action_breakdowns=action_breakdowns,
        action_report_time=action_report_time,
        breakdowns=breakdowns,
        default_summary=default_summary,
        use_account_attribution_setting=use_account_attribution_setting,
        use_unified_attribution_setting=use_unified_attribution_setting,
        filtering=filtering,
        sort=sort,
        limit=limit,
        after=after,
        before=before,
        offset=offset,
        since=since,
        until=until,
        locale=locale
    )

    return _make_graph_api_call(url, params)

@mcp.tool()
def get_campaign_insights(
    campaign_id: str,
    fields: Optional[List[str]] = None,
    date_preset: str = 'last_30d',
    time_range: Optional[Dict[str, str]] = None,
    time_ranges: Optional[List[Dict[str, str]]] = None,
    time_increment: str = 'all_days',
    action_attribution_windows: Optional[List[str]] = None,
    action_breakdowns: Optional[List[str]] = None,
    action_report_time: Optional[str] = None,
    breakdowns: Optional[List[str]] = None,
    default_summary: bool = False,
    use_account_attribution_setting: bool = False,
    use_unified_attribution_setting: bool = True,
    level: Optional[str] = None,
    filtering: Optional[List[dict]] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    offset: Optional[int] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    locale: Optional[str] = None
) -> Dict:
    """Retrieves performance insights for a specific Facebook ad campaign.

    Fetches statistics for a given campaign ID, allowing analysis of metrics like
    impressions, clicks, conversions, spend, etc. Supports time range definitions,
    breakdowns, and attribution settings.

    Args:
        campaign_id (str): The ID of the target Facebook ad campaign, e.g., '23843xxxxx'.
        fields (Optional[List[str]]): A list of specific metrics and fields to retrieve.
            Common examples: 'campaign_name', 'account_id', 'impressions', 'clicks',
            'spend', 'ctr', 'reach', 'actions', 'objective', 'cost_per_action_type',
            'conversions', 'cpc', 'cpm', 'cpp', 'frequency', 'date_start', 'date_stop'.
        date_preset (str): A predefined relative time range for the report.
            Options: 'today', 'yesterday', 'this_month', 'last_month', 'this_quarter',
            'maximum', 'last_3d', 'last_7d', 'last_14d', 'last_28d', 'last_30d',
            'last_90d', 'last_week_mon_sun', 'last_week_sun_sat', 'last_quarter',
            'last_year', 'this_week_mon_today', 'this_week_sun_today', 'this_year'.
            Default: 'last_30d'. Ignored if 'time_range', 'time_ranges', 'since', or 'until' is used.
        time_range (Optional[Dict[str, str]]): A specific time range {'since':'YYYY-MM-DD','until':'YYYY-MM-DD'}.
            Overrides 'date_preset'. Ignored if 'time_ranges' is provided.
        time_ranges (Optional[List[Dict[str, str]]]): An array of time range objects for comparison.
            Overrides 'time_range' and 'date_preset'.
        time_increment (str | int): Specifies the granularity of the time breakdown.
            - Integer (1-90): number of days per data point.
            - 'monthly': Aggregates data by month.
            - 'all_days': Single summary row for the period.
            Default: 'all_days'.
        action_attribution_windows (Optional[List[str]]): Specifies attribution windows for actions.
            Examples: '1d_view', '7d_click', '28d_click', etc. Default depends on API/settings.
        action_breakdowns (Optional[List[str]]): Segments 'actions' results. Examples: 'action_device', 'action_type'.
            Default: ['action_type'].
        action_report_time (Optional[str]): Determines when actions are counted ('impression', 'conversion', 'mixed').
            Default: 'mixed'.
        breakdowns (Optional[List[str]]): Segments results by dimensions. Examples: 'age', 'gender', 'country',
            'publisher_platform', 'impression_device'.
        default_summary (bool): If True, includes an additional summary row. Default: False.
        use_account_attribution_setting (bool): If True, uses the ad account's attribution settings. Default: False.
        use_unified_attribution_setting (bool): If True, uses unified attribution settings. Default: True.
        level (Optional[str]): Level of aggregation ('campaign', 'adset', 'ad'). Default: 'campaign'.
        filtering (Optional[List[dict]]): List of filter objects {'field': '...', 'operator': '...', 'value': '...'}.
        sort (Optional[str]): Field and direction for sorting ('{field}_ascending'/'_descending').
        limit (Optional[int]): Maximum number of results per page.
        after (Optional[str]): Pagination cursor for the next page.
        before (Optional[str]): Pagination cursor for the previous page.
        offset (Optional[int]): Alternative pagination: skips N results.
        since (Optional[str]): Start timestamp for time-based pagination (if time ranges absent).
        until (Optional[str]): End timestamp for time-based pagination (if time ranges absent).
        locale (Optional[str]): The locale for text responses (e.g., 'en_US'). This controls 
            language and formatting of text fields in the response.

    Returns:
        Dict: A dictionary containing the requested campaign insights, with 'data' and 'paging' keys.

    Example:
        ```python
        # Get basic campaign performance for the last 7 days
        insights = get_campaign_insights(
            campaign_id="23843xxxxx",
            fields=["campaign_name", "impressions", "clicks", "spend"],
            date_preset="last_7d",
            limit=50
        )

        # Fetch the next page if available
        next_page_url = insights.get("paging", {}).get("next")
        if next_page_url:
            next_page_results = fetch_pagination_url(url=next_page_url)
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}/insights"
    params = {'access_token': access_token}

    # Default level to 'campaign' if not provided for this specific tool
    effective_level = level if level else 'campaign'

    params = _build_insights_params(
        params=params,
        fields=fields,
        date_preset=date_preset,
        time_range=time_range,
        time_ranges=time_ranges,
        time_increment=time_increment,
        level=effective_level,
        action_attribution_windows=action_attribution_windows,
        action_breakdowns=action_breakdowns,
        action_report_time=action_report_time,
        breakdowns=breakdowns,
        default_summary=default_summary,
        use_account_attribution_setting=use_account_attribution_setting,
        use_unified_attribution_setting=use_unified_attribution_setting,
        filtering=filtering,
        sort=sort,
        limit=limit,
        after=after,
        before=before,
        offset=offset,
        since=since,
        until=until,
        locale=locale
    )
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_adset_insights(
    adset_id: str,
    fields: Optional[List[str]] = None,
    date_preset: str = 'last_30d',
    time_range: Optional[Dict[str, str]] = None,
    time_ranges: Optional[List[Dict[str, str]]] = None,
    time_increment: str = 'all_days',
    action_attribution_windows: Optional[List[str]] = None,
    action_breakdowns: Optional[List[str]] = None,
    action_report_time: Optional[str] = None,
    breakdowns: Optional[List[str]] = None,
    default_summary: bool = False,
    use_account_attribution_setting: bool = False,
    use_unified_attribution_setting: bool = True,
    level: Optional[str] = None,
    filtering: Optional[List[dict]] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    offset: Optional[int] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    locale: Optional[str] = None
) -> Dict:
    """Retrieves performance insights for a specific Facebook ad set.

    Provides advertising performance statistics for an ad set, allowing for analysis
    of metrics across its child ads. Supports time range definitions, breakdowns,
    filtering, sorting, and attribution settings. Some metrics may be estimated
    or in development.
    
    Args:
        adset_id (str): The ID of the target ad set, e.g., '6123456789012'.
        fields (Optional[List[str]]): A list of specific metrics and fields. Common examples:
            'adset_name', 'campaign_name', 'account_id', 'impressions', 'clicks', 'spend',
            'ctr', 'reach', 'frequency', 'actions', 'conversions', 'cpc', 'cpm', 'cpp',
            'cost_per_action_type', 'video_p25_watched_actions', 'website_purchases'.
        date_preset (str): A predefined relative time range ('last_30d', 'last_7d', etc.).
            Default: 'last_30d'. Ignored if 'time_range', 'time_ranges', 'since', or 'until' is used.
        time_range (Optional[Dict[str, str]]): Specific time range {'since':'YYYY-MM-DD','until':'YYYY-MM-DD'}.
            Overrides 'date_preset'. Ignored if 'time_ranges' is provided.
        time_ranges (Optional[List[Dict[str, str]]]): Array of time range objects for comparison.
            Overrides 'time_range' and 'date_preset'.
        time_increment (str | int): Granularity of the time breakdown ('all_days', 'monthly', 1-90 days).
            Default: 'all_days'.
        action_attribution_windows (Optional[List[str]]): Specifies attribution windows for actions.
            Examples: '1d_view', '7d_click'. Default depends on API/settings.
        action_breakdowns (Optional[List[str]]): Segments 'actions' results. Examples: 'action_device', 'action_type'.
            Default: ['action_type'].
        action_report_time (Optional[str]): Time basis for action stats ('impression', 'conversion', 'mixed').
            Default: 'mixed'.
        breakdowns (Optional[List[str]]): Segments results by dimensions. Examples: 'age', 'gender', 'country',
            'publisher_platform', 'impression_device', 'platform_position'.
        default_summary (bool): If True, includes an additional summary row. Default: False.
        use_account_attribution_setting (bool): If True, uses the ad account's attribution settings. Default: False.
        use_unified_attribution_setting (bool): If True, uses unified attribution settings. Default: True.
        level (Optional[str]): Level of aggregation ('adset', 'ad'). Default: 'adset'.
        filtering (Optional[List[dict]]): List of filter objects {'field': '...', 'operator': '...', 'value': '...'}.
        sort (Optional[str]): Field and direction for sorting ('{field}_ascending'/'_descending').
        limit (Optional[int]): Maximum number of results per page.
        after (Optional[str]): Pagination cursor for the next page.
        before (Optional[str]): Pagination cursor for the previous page.
        offset (Optional[int]): Alternative pagination: skips N results.
        since (Optional[str]): Start timestamp for time-based pagination (if time ranges absent).
        until (Optional[str]): End timestamp for time-based pagination (if time ranges absent).
        locale (Optional[str]): The locale for text responses (e.g., 'en_US'). This controls 
            language and formatting of text fields in the response.
    
    Returns:    
        Dict: A dictionary containing the requested ad set insights, with 'data' and 'paging' keys.

    Example:
        ```python
        # Get ad set performance with breakdown by device for last 14 days
        insights = get_adset_insights(
            adset_id="6123456789012",
            fields=["adset_name", "impressions", "spend"],
            breakdowns=["impression_device"],
            date_preset="last_14d"
        )

        # Fetch the next page if available
        next_page_url = insights.get("paging", {}).get("next")
        if next_page_url:
            next_page_results = fetch_pagination_url(url=next_page_url)
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}/insights"
    params = {'access_token': access_token}

    # Default level to 'adset' if not provided for this specific tool
    effective_level = level if level else 'adset'

    params = _build_insights_params(
        params=params,
        fields=fields,
        date_preset=date_preset,
        time_range=time_range,
        time_ranges=time_ranges,
        time_increment=time_increment,
        level=effective_level,
        action_attribution_windows=action_attribution_windows,
        action_breakdowns=action_breakdowns,
        action_report_time=action_report_time,
        breakdowns=breakdowns,
        default_summary=default_summary,
        use_account_attribution_setting=use_account_attribution_setting,
        use_unified_attribution_setting=use_unified_attribution_setting,
        filtering=filtering,
        sort=sort,
        limit=limit,
        after=after,
        before=before,
        offset=offset,
        since=since,
        until=until,
        locale=locale
    )

    return _make_graph_api_call(url, params)


@mcp.tool()
def get_ad_insights(
    ad_id: str,
    fields: Optional[List[str]] = None,
    date_preset: str = 'last_30d',
    time_range: Optional[Dict[str, str]] = None,
    time_ranges: Optional[List[Dict[str, str]]] = None,
    time_increment: str = 'all_days',
    action_attribution_windows: Optional[List[str]] = None,
    action_breakdowns: Optional[List[str]] = None,
    action_report_time: Optional[str] = None,
    breakdowns: Optional[List[str]] = None,
    default_summary: bool = False,
    use_account_attribution_setting: bool = False,
    use_unified_attribution_setting: bool = True,
    level: Optional[str] = None,
    filtering: Optional[List[dict]] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    offset: Optional[int] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    locale: Optional[str] = None
) -> Dict:  
    """Retrieves detailed performance insights for a specific Facebook ad.

    Fetches performance metrics for an individual ad (ad group), such as impressions,
    clicks, conversions, engagement, video views, etc. Allows for customization via
    time periods, breakdowns, filtering, sorting, and attribution settings. Note that
    some metrics may be estimated or in development.
    
    Args:
        ad_id (str): The ID of the target ad (ad group), e.g., '6123456789012'.
        fields (Optional[List[str]]): A list of specific metrics and fields. Common examples:
            'ad_name', 'adset_name', 'campaign_name', 'account_id', 'impressions', 'clicks',
            'spend', 'ctr', 'cpc', 'cpm', 'cpp', 'reach', 'frequency', 'actions', 'conversions',
            'cost_per_action_type', 'inline_link_clicks', 'inline_post_engagement', 'unique_clicks',
            'video_p25_watched_actions', 'video_p50_watched_actions', 'video_p75_watched_actions',
            'video_p95_watched_actions', 'video_p100_watched_actions', 'video_avg_time_watched_actions',
            'website_ctr', 'website_purchases'.
        date_preset (str): A predefined relative time range ('last_30d', 'last_7d', etc.).
            Default: 'last_30d'. Ignored if 'time_range', 'time_ranges', 'since', or 'until' is used.
        time_range (Optional[Dict[str, str]]): Specific time range {'since':'YYYY-MM-DD','until':'YYYY-MM-DD'}.
            Overrides 'date_preset'. Ignored if 'time_ranges' is provided.
        time_ranges (Optional[List[Dict[str, str]]]): Array of time range objects for comparison.
            Overrides 'time_range' and 'date_preset'.
        time_increment (str | int): Granularity of the time breakdown ('all_days', 'monthly', 1-90 days).
            Default: 'all_days'.
        action_attribution_windows (Optional[List[str]]): Specifies attribution windows for actions.
            Examples: '1d_view', '7d_click'. Default depends on API/settings.
        action_breakdowns (Optional[List[str]]): Segments 'actions' results. Examples: 'action_device', 'action_type'.
            Default: ['action_type'].
        action_report_time (Optional[str]): Time basis for action stats ('impression', 'conversion', 'mixed').
            Default: 'mixed'.
        breakdowns (Optional[List[str]]): Segments results by dimensions. Examples: 'age', 'gender', 'country',
            'publisher_platform', 'impression_device', 'platform_position', 'device_platform'.
        default_summary (bool): If True, includes an additional summary row. Default: False.
        use_account_attribution_setting (bool): If True, uses the ad account's attribution settings. Default: False.
        use_unified_attribution_setting (bool): If True, uses unified attribution settings. Default: True.
        level (Optional[str]): Level of aggregation. Should typically be 'ad'. Default: 'ad'.
        filtering (Optional[List[dict]]): List of filter objects {'field': '...', 'operator': '...', 'value': '...'}.
        sort (Optional[str]): Field and direction for sorting ('{field}_ascending'/'_descending').
        limit (Optional[int]): Maximum number of results per page.
        after (Optional[str]): Pagination cursor for the next page.
        before (Optional[str]): Pagination cursor for the previous page.
        offset (Optional[int]): Alternative pagination: skips N results.
        since (Optional[str]): Start timestamp for time-based pagination (if time ranges absent).
        until (Optional[str]): End timestamp for time-based pagination (if time ranges absent).
        locale (Optional[str]): The locale for text responses (e.g., 'en_US'). This controls 
            language and formatting of text fields in the response.
    
    Returns:    
        Dict: A dictionary containing the requested ad insights, with 'data' and 'paging' keys.
        
    Example:
        ```python
        # Get basic ad performance for the last 30 days
        ad_insights = get_ad_insights(
            ad_id="6123456789012", 
            fields=["ad_name", "impressions", "clicks", "spend", "ctr", "reach"],
            limit=10
        )
        
        # Get ad performance with platform breakdown for last 14 days
        platform_insights = get_ad_insights(
            ad_id="6123456789012",
            fields=["ad_name", "impressions", "clicks", "spend"],
            breakdowns=["publisher_platform", "platform_position"],
            date_preset="last_14d"
        )
        
        # Fetch the next page of basic performance if available
        next_page_url = ad_insights.get("paging", {}).get("next")
        if next_page_url:
            next_page = fetch_pagination_url(url=next_page_url)
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}/insights"
    params = {'access_token': access_token}

    # Default level to 'ad' if not provided for this specific tool
    effective_level = level if level else 'ad'

    params = _build_insights_params(
        params=params,
        fields=fields,
        date_preset=date_preset,
        time_range=time_range,
        time_ranges=time_ranges,
        time_increment=time_increment,
        level=effective_level,
        action_attribution_windows=action_attribution_windows,
        action_breakdowns=action_breakdowns,
        action_report_time=action_report_time,
        breakdowns=breakdowns,
        default_summary=default_summary,
        use_account_attribution_setting=use_account_attribution_setting,
        use_unified_attribution_setting=use_unified_attribution_setting,
        filtering=filtering,
        sort=sort,
        limit=limit,
        after=after,
        before=before,
        offset=offset,
        since=since,
        until=until,
        locale=locale
    )

    return _make_graph_api_call(url, params)


@mcp.tool()
def fetch_pagination_url(url: str) -> Dict:
    """Fetch data from a Facebook Graph API pagination URL
    
    Use this to get the next/previous page of results from an insights API call.
    
    Args:
        url: The complete pagination URL (e.g., from response['paging']['next'] or response['paging']['previous']).
             It includes the necessary token and parameters.
             
    Returns:
        The dictionary containing the next/previous page of results.
        
    Example:
        ```python
        # Assuming 'initial_results' is the dict from a previous insights call
        if "paging" in initial_results and "next" in initial_results["paging"]:
            next_page_data = fetch_pagination_url(url=initial_results["paging"]["next"])

        if "paging" in initial_results and "previous" in initial_results["paging"]:
            prev_page_data = fetch_pagination_url(url=initial_results["paging"]["previous"])
        ```
    """
    # This function takes a full URL which already includes the access token,
    # so we don't use the _make_graph_api_call helper here.
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# --- Ad Creative Tools ---

@mcp.tool()
def get_ad_creative_by_id(
    creative_id: str, 
    fields: Optional[List[str]] = None,
    thumbnail_width: Optional[int] = None, 
    thumbnail_height: Optional[int] = None
) -> Dict:
    """Retrieves detailed information about a specific Facebook ad creative.

    This tool interfaces with the Facebook Graph API to fetch comprehensive details
    about an ad creative, such as its name, status, specifications, engagement metrics,
    and associated objects (like images, videos, and pages).

    Args:
        creative_id (str): The ID of the ad creative to retrieve.
        fields (Optional[List[str]]): A list of specific fields to retrieve. If None, 
            returns the default set of fields. Available fields include (but are not limited to):
            - 'account_id': Ad account ID the creative belongs to
            - 'actor_id': ID of the Facebook actor (page/app/person) associated with this creative
            - 'adlabels': Ad labels associated with this creative
            - 'applink_treatment': App link treatment type
            - 'asset_feed_spec': Specifications for dynamic ad creatives
            - 'authorization_category': For political ads, shows authorization category
            - 'body': Ad body text content
            - 'branded_content_sponsor_page_id': ID of the sponsor page for branded content
            - 'call_to_action_type': Type of call to action button
            - 'effective_authorization_category': Effective authorization category for the ad
            - 'effective_instagram_media_id': Instagram media ID used in the ad
            - 'effective_instagram_story_id': Instagram story ID used in the ad
            - 'effective_object_story_id': Object story ID used for the ad
            - 'id': Creative ID
            - 'image_hash': Hash of the image used in the creative
            - 'image_url': URL of the image used
            - 'instagram_actor_id': Instagram actor ID associated with creative (deprecated)
            - 'instagram_permalink_url': Instagram permalink URL
            - 'instagram_story_id': Instagram story ID
            - 'instagram_user_id': Instagram user ID associated with creative
            - 'link_og_id': Open Graph ID for the link
            - 'link_url': URL being advertised
            - 'name': Name of the creative in the ad account library
            - 'object_id': ID of the Facebook object being advertised
            - 'object_story_id': ID of the page post used in the ad
            - 'object_story_spec': Specification for the page post to create for the ad
            - 'object_type': Type of the object being advertised
            - 'object_url': URL of the object being advertised
            - 'platform_customizations': Custom specifications for different platforms
            - 'product_set_id': ID of the product set for product ads
            - 'status': Status of this creative (ACTIVE, IN_PROCESS, WITH_ISSUES, DELETED)
            - 'template_url': URL of the template used
            - 'thumbnail_url': URL of the creative thumbnail
            - 'title': Ad headline/title text
            - 'url_tags': URL tags appended to landing pages for tracking
            - 'use_page_actor_override': Use the page actor instead of ad account actor
            - 'video_id': ID of the video used in the ad
        
        thumbnail_width (Optional[int]): Width of the thumbnail in pixels. Default: 64.
        thumbnail_height (Optional[int]): Height of the thumbnail in pixels. Default: 64.

    Returns:
        Dict: A dictionary containing the requested ad creative details.

    Example:
        ```python
        # Get basic information about an ad creative
        creative = get_ad_creative_details(
            creative_id="23842312323312",
            fields=["name", "status", "object_story_id", "thumbnail_url"]
        )
        
        # Get a larger thumbnail with specific dimensions
        creative_with_thumbnail = get_ad_creative_details(
            creative_id="23842312323312", 
            fields=["name", "thumbnail_url"],
            thumbnail_width=300,
            thumbnail_height=200
        )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{creative_id}"
    params = {'access_token': access_token}
    
    # Add requested fields
    if fields:
        params['fields'] = ','.join(fields)
    
    # Add thumbnail dimensions if specified
    if thumbnail_width:
        params['thumbnail_width'] = thumbnail_width
    if thumbnail_height:
        params['thumbnail_height'] = thumbnail_height
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_ad_creatives_by_ad_id(
    ad_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    date_format: Optional[str] = None
) -> Dict:
    """Retrieves the ad creatives associated with a specific Facebook ad.
    
    This function accesses the Facebook Graph API to retrieve the creative objects
    used by a specific ad, including details about the creative content, media, 
    and specifications.
    
    Args:
        ad_id (str): The ID of the ad to retrieve creatives for.
        fields (Optional[List[str]]): A list of specific fields to retrieve for each creative.
            If None, a default set of fields will be returned. Available fields include:
            - 'id': The creative's ID
            - 'name': The creative's name
            - 'account_id': The ID of the ad account this creative belongs to
            - 'actor_id': ID of the Facebook actor associated with creative
            - 'adlabels': Ad labels applied to the creative
            - 'applink_treatment': App link treatment type
            - 'asset_feed_spec': Specifications for dynamic ad creatives
            - 'authorization_category': Political ad authorization category
            - 'body': Ad body text content
            - 'branded_content_sponsor_page_id': ID of sponsoring page for branded content
            - 'call_to_action_type': Type of call to action button
            - 'effective_authorization_category': Effective authorization category
            - 'effective_instagram_media_id': Instagram media ID used
            - 'effective_instagram_story_id': Instagram story ID used
            - 'effective_object_story_id': Object story ID used
            - 'image_hash': Hash of the image used in the creative
            - 'image_url': URL of the image used
            - 'instagram_actor_id': Instagram actor ID (deprecated)
            - 'instagram_permalink_url': Instagram permalink URL
            - 'instagram_story_id': Instagram story ID
            - 'instagram_user_id': Instagram user ID associated with creative
            - 'link_og_id': Open Graph ID for the link
            - 'link_url': URL being advertised
            - 'object_id': ID of the Facebook object being advertised
            - 'object_story_id': ID of the page post used in the ad
            - 'object_story_spec': Specification for the page post 
            - 'object_type': Type of the object being advertised ('PAGE', 'DOMAIN', etc.)
            - 'object_url': URL of the object being advertised
            - 'platform_customizations': Custom specifications for different platforms
            - 'product_set_id': ID of the product set for product ads
            - 'status': Status of this creative ('ACTIVE', 'IN_PROCESS', etc.)
            - 'template_url': URL of the template used
            - 'thumbnail_url': URL of the creative thumbnail
            - 'title': Ad headline/title text
            - 'url_tags': URL tags appended to landing pages for tracking
            - 'use_page_actor_override': Whether to use the page actor instead of account actor
            - 'video_id': ID of the video used in the ad
        limit (Optional[int]): Maximum number of creatives to return per page. Default is 25.
        after (Optional[str]): Pagination cursor for the next page. From response['paging']['cursors']['after'].
        before (Optional[str]): Pagination cursor for the previous page. From response['paging']['cursors']['before'].
        date_format (Optional[str]): Format for date responses. Options:
            - 'U': Unix timestamp (seconds since epoch)
            - 'Y-m-d H:i:s': MySQL datetime format
            - None: ISO 8601 format (default)
    
    Returns:
        Dict: A dictionary containing the requested ad creatives. The main results are in the 'data'
              list, and pagination info is in the 'paging' object.
    
    Example:
        ```python
        # Get basic creative information for an ad
        creatives = get_ad_creatives(
            ad_id="23843211234567",
            fields=["name", "image_url", "body", "title", "status"]
        )
        
        # Get detailed creative specifications with pagination
        detailed_creatives = get_ad_creatives(
            ad_id="23843211234567",
            fields=["name", "object_story_spec", "image_url", "call_to_action_type"],
            limit=50
        )
        
        # Fetch the next page if available using the pagination cursor
        next_page_cursor = creatives.get("paging", {}).get("cursors", {}).get("after")
        if next_page_cursor:
            next_page = get_ad_creatives(
                ad_id="23843211234567",
                fields=["name", "image_url", "body", "title"],
                limit=50,
                after=next_page_cursor
            )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}/adcreatives"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
        
    if date_format:
        params['date_format'] = date_format
    
    return _make_graph_api_call(url, params)


# --- Ad Tools ---

@mcp.tool()
def get_ad_by_id(ad_id: str, fields: Optional[List[str]] = None) -> Dict:
    """Retrieves detailed information about a specific Facebook ad by its ID.
    
    This function accesses the Facebook Graph API to retrieve information about a
    single ad object, including details about its status, targeting, creative, budget,
    and performance metrics.
    
    Args:
        ad_id (str): The ID of the ad to retrieve information for.
        fields (Optional[List[str]]): A list of specific fields to retrieve. If None,
            a default set of fields will be returned. Available fields include:
            - 'id': The ad's ID
            - 'name': The ad's name
            - 'account_id': The ID of the ad account this ad belongs to
            - 'adset_id': The ID of the ad set this ad belongs to
            - 'campaign_id': The ID of the campaign this ad belongs to
            - 'adlabels': Labels applied to the ad
            - 'bid_amount': The bid amount for this ad
            - 'bid_type': The bid type of this ad
            - 'bid_info': The bid info for this ad
            - 'configured_status': The configured status of this ad
            - 'conversion_domain': The conversion domain for this ad
            - 'created_time': When the ad was created
            - 'creative': The ad creative
            - 'effective_status': The effective status of this ad
            - 'issues_info': Information about issues with this ad
            - 'recommendations': Recommendations for improving this ad
            - 'status': The status of this ad
            - 'tracking_specs': The tracking specs for this ad
            - 'updated_time': When this ad was last updated
            - 'preview_shareable_link': Link for previewing this ad
    
    Returns:
        Dict: A dictionary containing the requested ad information.
    
    Example:
        ```python
        # Get basic ad information
        ad = get_ad_by_id(
            ad_id="23843211234567",
            fields=["name", "adset_id", "campaign_id", "effective_status", "creative"]
        )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_ads_by_adaccount(
    act_id: str,
    fields: Optional[List[str]] = None,
    filtering: Optional[List[dict]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    date_preset: Optional[str] = None,
    time_range: Optional[Dict[str, str]] = None,
    updated_since: Optional[int] = None,
    effective_status: Optional[List[str]] = None
) -> Dict:
    """Retrieves ads from a specific Facebook ad account.
    
    This function allows querying all ads belonging to a specific ad account with
    various filtering options, pagination, and field selection.
    
    Args:
        act_id (str): The ID of the ad account to retrieve ads from, prefixed with 'act_', 
                      e.g., 'act_1234567890'.
        fields (Optional[List[str]]): A list of specific fields to retrieve for each ad. 
                                      If None, a default set of fields will be returned.
                                      Common fields include:
            - 'id': The ad's ID
            - 'name': The ad's name
            - 'adset_id': The ID of the ad set this ad belongs to
            - 'campaign_id': The ID of the campaign this ad belongs to
            - 'creative': The ad creative details
            - 'status': The current status of the ad
            - 'effective_status': The effective status including review status
            - 'bid_amount': The bid amount for this ad
            - 'configured_status': The configured status
            - 'created_time': When the ad was created
            - 'updated_time': When the ad was last updated
            - 'targeting': Targeting criteria
            - 'conversion_specs': Conversion specs
            - 'recommendations': Recommendations for improving the ad
            - 'preview_shareable_link': Link for previewing the ad
        filtering (Optional[List[dict]]): A list of filter objects to apply to the data.
                                         Each object should have 'field', 'operator', and 'value' keys.
        limit (Optional[int]): Maximum number of ads to return per page. Default is 25.
        after (Optional[str]): Pagination cursor for the next page. From response['paging']['cursors']['after'].
        before (Optional[str]): Pagination cursor for the previous page. From response['paging']['cursors']['before'].
        date_preset (Optional[str]): A predefined relative date range for selecting ads.
                                    Options include 'today', 'yesterday', 'this_week', etc.
        time_range (Optional[Dict[str, str]]): A custom time range with 'since' and 'until' 
                                              dates in 'YYYY-MM-DD' format.
        updated_since (Optional[int]): Return ads that have been updated since this Unix timestamp.
        effective_status (Optional[List[str]]): Filter ads by their effective status. 
                                               Options include: 'ACTIVE', 'PAUSED', 'DELETED', 
                                               'PENDING_REVIEW', 'DISAPPROVED', 'PREAPPROVED', 
                                               'PENDING_BILLING_INFO', 'CAMPAIGN_PAUSED', 'ARCHIVED', 
                                               'ADSET_PAUSED', 'IN_PROCESS', 'WITH_ISSUES'.
    
    Returns:
        Dict: A dictionary containing the requested ads. The main results are in the 'data'
              list, and pagination info is in the 'paging' object.
    
    Example:
        ```python
        # Get active ads from an ad account
        ads = get_ads_by_adaccount(
            act_id="act_123456789",
            fields=["name", "adset_id", "campaign_id", "effective_status", "created_time"],
            effective_status=["ACTIVE"],
            limit=50
        )
        
        # Fetch the next page if available using the pagination cursor
        next_page_cursor = ads.get("paging", {}).get("cursors", {}).get("after")
        if next_page_cursor:
            next_page = get_ads_by_adaccount(
                act_id="act_123456789",
                fields=["name", "adset_id", "campaign_id", "effective_status", "created_time"],
                effective_status=["ACTIVE"],
                limit=50,
                after=next_page_cursor
            )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/ads"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if filtering:
        params['filtering'] = json.dumps(filtering)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
    
    if date_preset:
        params['date_preset'] = date_preset
    
    if time_range:
        params['time_range'] = json.dumps(time_range)
    
    if updated_since:
        params['updated_since'] = updated_since
    
    if effective_status:
        params['effective_status'] = json.dumps(effective_status)
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_ads_by_campaign(
    campaign_id: str,
    fields: Optional[List[str]] = None,
    filtering: Optional[List[dict]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    effective_status: Optional[List[str]] = None
) -> Dict:
    """Retrieves ads associated with a specific Facebook campaign.
    
    This function allows querying all ads belonging to a specific campaign,
    with filtering options, pagination, and field selection.
    
    Args:
        campaign_id (str): The ID of the campaign to retrieve ads from.
        fields (Optional[List[str]]): A list of specific fields to retrieve for each ad.
                                      If None, a default set of fields will be returned.
                                      Common fields include:
            - 'id': The ad's ID
            - 'name': The ad's name
            - 'adset_id': The ID of the ad set this ad belongs to
            - 'creative': The ad creative details
            - 'status': The current status of the ad
            - 'effective_status': The effective status including review status
            - 'bid_amount': The bid amount for this ad
            - 'created_time': When the ad was created
            - 'updated_time': When the ad was last updated
            - 'targeting': Targeting criteria
            - 'preview_shareable_link': Link for previewing the ad
        filtering (Optional[List[dict]]): A list of filter objects to apply to the data.
                                         Each object should have 'field', 'operator', and 'value' keys.
        limit (Optional[int]): Maximum number of ads to return per page. Default is 25.
        after (Optional[str]): Pagination cursor for the next page. From response['paging']['cursors']['after'].
        before (Optional[str]): Pagination cursor for the previous page. From response['paging']['cursors']['before'].
        effective_status (Optional[List[str]]): Filter ads by their effective status.
                                               Options include: 'ACTIVE', 'PAUSED', 'DELETED',
                                               'PENDING_REVIEW', 'DISAPPROVED', 'PREAPPROVED',
                                               'PENDING_BILLING_INFO', 'ADSET_PAUSED', 'ARCHIVED',
                                               'IN_PROCESS', 'WITH_ISSUES'.
    
    Returns:
        Dict: A dictionary containing the requested ads. The main results are in the 'data'
              list, and pagination info is in the 'paging' object.
    
    Example:
        ```python
        # Get all active ads from a campaign
        ads = get_ads_by_campaign(
            campaign_id="23843211234567",
            fields=["name", "adset_id", "effective_status", "created_time"],
            effective_status=["ACTIVE"],
            limit=50
        )
        
        # Fetch the next page if available using the pagination cursor
        next_page_cursor = ads.get("paging", {}).get("cursors", {}).get("after")
        if next_page_cursor:
            next_page = get_ads_by_campaign(
                campaign_id="23843211234567",
                fields=["name", "adset_id", "effective_status", "created_time"],
                effective_status=["ACTIVE"],
                limit=50,
                after=next_page_cursor
            )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}/ads"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if filtering:
        params['filtering'] = json.dumps(filtering)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
    
    if effective_status:
        params['effective_status'] = json.dumps(effective_status)
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_ads_by_adset(
    adset_id: str,
    fields: Optional[List[str]] = None,
    filtering: Optional[List[dict]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    effective_status: Optional[List[str]] = None,
    date_format: Optional[str] = None
) -> Dict:
    """Retrieves ads associated with a specific Facebook ad set.
    
    This function allows querying all ads belonging to a specific ad set,
    with filtering options, pagination, and field selection.
    
    Args:
        adset_id (str): The ID of the ad set to retrieve ads from.
        fields (Optional[List[str]]): A list of specific fields to retrieve for each ad.
                                      If None, a default set of fields will be returned.
                                      See get_ad_by_id for a comprehensive list of available fields.
        filtering (Optional[List[dict]]): A list of filter objects to apply to the data.
                                         Each object should have 'field', 'operator', and 'value' keys.
                                         Operators include: 'EQUAL', 'NOT_EQUAL', 'GREATER_THAN',
                                         'GREATER_THAN_OR_EQUAL', 'LESS_THAN', 'LESS_THAN_OR_EQUAL',
                                         'IN_RANGE', 'NOT_IN_RANGE', 'CONTAIN', 'NOT_CONTAIN',
                                         'IN', 'NOT_IN', 'EMPTY', 'NOT_EMPTY'.
        limit (Optional[int]): Maximum number of ads to return per page. Default is 25, max is 100.
        after (Optional[str]): Pagination cursor for the next page. From response['paging']['cursors']['after'].
        before (Optional[str]): Pagination cursor for the previous page. From response['paging']['cursors']['before'].
        effective_status (Optional[List[str]]): Filter ads by their effective status.
                                               Options include: 'ACTIVE', 'PAUSED', 'DELETED',
                                               'PENDING_REVIEW', 'DISAPPROVED', 'PREAPPROVED',
                                               'PENDING_BILLING_INFO', 'CAMPAIGN_PAUSED', 'ARCHIVED',
                                               'IN_PROCESS', 'WITH_ISSUES'.
        date_format (Optional[str]): Format for date responses. Options:
                                    - 'U': Unix timestamp (seconds since epoch)
                                    - 'Y-m-d H:i:s': MySQL datetime format
                                    - None: ISO 8601 format (default)
    
    Returns:
        Dict: A dictionary containing the requested ads. The main results are in the 'data'
              list, and pagination info is in the 'paging' object.
    
    Example:
        ```python
        # Get all active ads from an ad set
        ads = get_ads_by_adset(
            adset_id="23843211234567",
            fields=["name", "campaign_id", "effective_status", "created_time", "creative"],
            effective_status=["ACTIVE"],
            limit=50
        )
        
        # Get ads with specific fields and date format
        time_ads = get_ads_by_adset(
            adset_id="23843211234567",
            fields=["name", "created_time", "updated_time", "status"],
            date_format="Y-m-d H:i:s"
        )
        
        # Fetch the next page if available using the pagination cursor
        next_page_cursor = ads.get("paging", {}).get("cursors", {}).get("after")
        if next_page_cursor:
            next_page = get_ads_by_adset(
                adset_id="23843211234567",
                fields=["name", "campaign_id", "effective_status", "created_time", "creative"],
                effective_status=["ACTIVE"],
                limit=50,
                after=next_page_cursor
            )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}/ads"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if filtering:
        params['filtering'] = json.dumps(filtering)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
    
    if effective_status:
        params['effective_status'] = json.dumps(effective_status)
        
    if date_format:
        params['date_format'] = date_format
    
    return _make_graph_api_call(url, params)


# --- Ad Set Tools ---

@mcp.tool()
def get_adset_by_id(adset_id: str, fields: Optional[List[str]] = None) -> Dict:
    """Retrieves detailed information about a specific Facebook ad set by its ID.
    
    This function accesses the Facebook Graph API to retrieve information about a
    single ad set, including details about its targeting, budget, scheduling, and status.
    
    Args:
        adset_id (str): The ID of the ad set to retrieve information for.
        fields (Optional[List[str]]): A list of specific fields to retrieve. If None,
            a default set of fields will be returned. Available fields include:
            - 'id': The ad set's ID
            - 'name': The ad set's name
            - 'account_id': The ID of the ad account this ad set belongs to
            - 'campaign_id': The ID of the campaign this ad set belongs to
            - 'bid_amount': The bid amount for this ad set
            - 'bid_strategy': Strategy used for bidding. Options include: 'LOWEST_COST_WITHOUT_CAP', 
                'LOWEST_COST_WITH_BID_CAP', 'COST_CAP'
            - 'billing_event': The billing event type. Options include: 'APP_INSTALLS', 
                'CLICKS', 'IMPRESSIONS', 'LINK_CLICKS', 'NONE', 'OFFER_CLAIMS', 
                'PAGE_LIKES', 'POST_ENGAGEMENT', 'THRUPLAY'
            - 'budget_remaining': The remaining budget for this ad set (in cents/smallest currency unit)
            - 'configured_status': The status set by the user. Options include: 'ACTIVE', 
                'PAUSED', 'DELETED', 'ARCHIVED'
            - 'created_time': When the ad set was created
            - 'daily_budget': The daily budget for this ad set (in cents/smallest currency unit)
            - 'daily_min_spend_target': The minimum daily spend target (in cents/smallest currency unit)
            - 'daily_spend_cap': The daily spend cap (in cents/smallest currency unit)
            - 'destination_type': Type of destination for the ads
            - 'effective_status': The effective status (actual status). Options include: 'ACTIVE', 
                'PAUSED', 'DELETED', 'PENDING_REVIEW', 'DISAPPROVED', 'PREAPPROVED', 
                'PENDING_BILLING_INFO', 'CAMPAIGN_PAUSED', 'ARCHIVED', 'ADSET_PAUSED', 
                'IN_PROCESS', 'WITH_ISSUES'
            - 'end_time': When the ad set will end (in ISO 8601 format)
            - 'frequency_control_specs': Specifications for frequency control
            - 'lifetime_budget': The lifetime budget (in cents/smallest currency unit)
            - 'lifetime_imps': The maximum number of lifetime impressions
            - 'lifetime_min_spend_target': The minimum lifetime spend target
            - 'lifetime_spend_cap': The lifetime spend cap
            - 'optimization_goal': The optimization goal for this ad set. Options include: 
                'APP_INSTALLS', 'BRAND_AWARENESS', 'CLICKS', 'ENGAGED_USERS', 'EVENT_RESPONSES', 
                'IMPRESSIONS', 'LEAD_GENERATION', 'LINK_CLICKS', 'NONE', 'OFFER_CLAIMS', 
                'OFFSITE_CONVERSIONS', 'PAGE_ENGAGEMENT', 'PAGE_LIKES', 'POST_ENGAGEMENT', 
                'QUALITY_LEAD', 'REACH', 'REPLIES', 'SOCIAL_IMPRESSIONS', 'THRUPLAY', 
                'VALUE', 'VISIT_INSTAGRAM_PROFILE'
            - 'pacing_type': List of pacing types. Options include: 'standard', 'no_pacing'
            - 'promoted_object': The object this ad set is promoting
            - 'recommendations': Recommendations for improving this ad set
            - 'rf_prediction_id': The Reach and Frequency prediction ID
            - 'source_adset_id': ID of the source ad set if this is a copy
            - 'start_time': When the ad set starts (in ISO 8601 format)
            - 'status': Deprecated. The ad set's status. Use 'effective_status' instead.
            - 'targeting': The targeting criteria for this ad set (complex object)
            - 'time_based_ad_rotation_id_blocks': Time-based ad rotation blocks
            - 'time_based_ad_rotation_intervals': Time-based ad rotation intervals in seconds
            - 'updated_time': When this ad set was last updated
            - 'use_new_app_click': Whether to use the newer app click tracking
    
    Returns:
        Dict: A dictionary containing the requested ad set information.
    
    Example:
        ```python
        # Get basic ad set information
        adset = get_adset_by_id(
            adset_id="23843211234567",
            fields=["name", "campaign_id", "effective_status", "targeting", "budget_remaining"]
        )
        
        # Get detailed scheduling information
        adset_schedule = get_adset_by_id(
            adset_id="23843211234567",
            fields=["name", "start_time", "end_time", "daily_budget", "lifetime_budget"]
        )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_adsets_by_ids(
    adset_ids: List[str],
    fields: Optional[List[str]] = None,
    date_format: Optional[str] = None
) -> Dict:
    """Retrieves detailed information about multiple Facebook ad sets by their IDs.
    
    This function allows batch retrieval of multiple ad sets in a single API call,
    improving efficiency when you need data for several ad sets.
    
    Args:
        adset_ids (List[str]): A list of ad set IDs to retrieve information for.
        fields (Optional[List[str]]): A list of specific fields to retrieve for each ad set.
            If None, a default set of fields will be returned. See get_adset_by_id for
            a comprehensive list of available fields.
        date_format (Optional[str]): Format for date responses. Options:
            - 'U': Unix timestamp (seconds since epoch)
            - 'Y-m-d H:i:s': MySQL datetime format
            - None: ISO 8601 format (default)
    
    Returns:
        Dict: A dictionary where keys are the ad set IDs and values are the
              corresponding ad set details.
    
    Example:
        ```python
        # Get information for multiple ad sets
        adsets = get_adsets_by_ids(
            adset_ids=["23843211234567", "23843211234568", "23843211234569"],
            fields=["name", "campaign_id", "effective_status", "budget_remaining"],
            date_format="U"  # Get dates as Unix timestamps
        )
        
        # Access information for a specific ad set
        if "23843211234567" in adsets:
            print(adsets["23843211234567"]["name"])
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/"
    params = {
        'access_token': access_token,
        'ids': ','.join(adset_ids)
    }
    
    if fields:
        params['fields'] = ','.join(fields)
        
    if date_format:
        params['date_format'] = date_format
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_adsets_by_adaccount(
    act_id: str,
    fields: Optional[List[str]] = None,
    filtering: Optional[List[dict]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    date_preset: Optional[str] = None,
    time_range: Optional[Dict[str, str]] = None,
    updated_since: Optional[int] = None,
    effective_status: Optional[List[str]] = None,
    date_format: Optional[str] = None
) -> Dict:
    """Retrieves ad sets from a specific Facebook ad account.
    
    This function allows querying all ad sets belonging to a specific ad account with
    various filtering options, pagination, and field selection.
    
    Args:
        act_id (str): The ID of the ad account to retrieve ad sets from, prefixed with 'act_', 
                      e.g., 'act_1234567890'.
        fields (Optional[List[str]]): A list of specific fields to retrieve for each ad set. 
                                      If None, a default set of fields will be returned.
                                      See get_adset_by_id for a comprehensive list of available fields.
        filtering (Optional[List[dict]]): A list of filter objects to apply to the data.
                                         Each object should have 'field', 'operator', and 'value' keys.
                                         Operators include: 'EQUAL', 'NOT_EQUAL', 'GREATER_THAN',
                                         'GREATER_THAN_OR_EQUAL', 'LESS_THAN', 'LESS_THAN_OR_EQUAL',
                                         'IN_RANGE', 'NOT_IN_RANGE', 'CONTAIN', 'NOT_CONTAIN',
                                         'IN', 'NOT_IN', 'EMPTY', 'NOT_EMPTY'.
                                         Example: [{'field': 'daily_budget', 'operator': 'GREATER_THAN', 'value': 1000}]
        limit (Optional[int]): Maximum number of ad sets to return per page. Default is 25, max is 100.
        after (Optional[str]): Pagination cursor for the next page. From response['paging']['cursors']['after'].
        before (Optional[str]): Pagination cursor for the previous page. From response['paging']['cursors']['before'].
        date_preset (Optional[str]): A predefined relative date range for selecting ad sets.
                                    Options include: 'today', 'yesterday', 'this_month', 'last_month', 
                                    'this_quarter', 'lifetime', 'last_3d', 'last_7d', 'last_14d', 
                                    'last_28d', 'last_30d', 'last_90d', 'last_quarter', 'last_year', 
                                    'this_week_mon_today', 'this_week_sun_today', 'this_year'.
        time_range (Optional[Dict[str, str]]): A custom time range with 'since' and 'until' 
                                              dates in 'YYYY-MM-DD' format.
                                              Example: {'since': '2023-01-01', 'until': '2023-01-31'}
        updated_since (Optional[int]): Return ad sets that have been updated since this Unix timestamp.
        effective_status (Optional[List[str]]): Filter ad sets by their effective status. 
                                               Options include: 'ACTIVE', 'PAUSED', 'DELETED', 
                                               'PENDING_REVIEW', 'DISAPPROVED', 'PREAPPROVED', 
                                               'PENDING_BILLING_INFO', 'CAMPAIGN_PAUSED', 'ARCHIVED', 
                                               'WITH_ISSUES'.
        date_format (Optional[str]): Format for date responses. Options:
                                    - 'U': Unix timestamp (seconds since epoch)
                                    - 'Y-m-d H:i:s': MySQL datetime format
                                    - None: ISO 8601 format (default)
    
    Returns:
        Dict: A dictionary containing the requested ad sets. The main results are in the 'data'
              list, and pagination info is in the 'paging' object.
    
    Example:
        ```python
        # Get active ad sets from an ad account
        adsets = get_adsets_by_adaccount(
            act_id="act_123456789",
            fields=["name", "campaign_id", "effective_status", "daily_budget", "targeting"],
            effective_status=["ACTIVE"],
            limit=50
        )
        
        # Get ad sets with daily budget above a certain amount
        high_budget_adsets = get_adsets_by_adaccount(
            act_id="act_123456789",
            fields=["name", "daily_budget", "lifetime_budget"],
            filtering=[{'field': 'daily_budget', 'operator': 'GREATER_THAN', 'value': 5000}],
            limit=100
        )
        
        # Fetch the next page if available using the pagination cursor
        next_page_cursor = adsets.get("paging", {}).get("cursors", {}).get("after")
        if next_page_cursor:
            next_page = get_adsets_by_adaccount(
                act_id="act_123456789",
                fields=["name", "campaign_id", "effective_status", "daily_budget"],
                effective_status=["ACTIVE"],
                limit=50,
                after=next_page_cursor
            )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/adsets"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if filtering:
        params['filtering'] = json.dumps(filtering)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
    
    if date_preset:
        params['date_preset'] = date_preset
    
    if time_range:
        params['time_range'] = json.dumps(time_range)
    
    if updated_since:
        params['updated_since'] = updated_since
    
    if effective_status:
        params['effective_status'] = json.dumps(effective_status)
        
    if date_format:
        params['date_format'] = date_format
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_adsets_by_campaign(
    campaign_id: str,
    fields: Optional[List[str]] = None,
    filtering: Optional[List[dict]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    effective_status: Optional[List[str]] = None,
    date_format: Optional[str] = None
) -> Dict:
    """Retrieves ad sets associated with a specific Facebook campaign.
    
    This function allows querying all ad sets belonging to a specific campaign,
    with filtering options, pagination, and field selection.
    
    Args:
        campaign_id (str): The ID of the campaign to retrieve ad sets from.
        fields (Optional[List[str]]): A list of specific fields to retrieve for each ad set.
                                      If None, a default set of fields will be returned.
                                      See get_adset_by_id for a comprehensive list of available fields.
        filtering (Optional[List[dict]]): A list of filter objects to apply to the data.
                                         Each object should have 'field', 'operator', and 'value' keys.
                                         Operators include: 'EQUAL', 'NOT_EQUAL', 'GREATER_THAN',
                                         'GREATER_THAN_OR_EQUAL', 'LESS_THAN', 'LESS_THAN_OR_EQUAL',
                                         'IN_RANGE', 'NOT_IN_RANGE', 'CONTAIN', 'NOT_CONTAIN',
                                         'IN', 'NOT_IN', 'EMPTY', 'NOT_EMPTY'.
                                         Example: [{'field': 'daily_budget', 'operator': 'GREATER_THAN', 'value': 1000}]
        limit (Optional[int]): Maximum number of ad sets to return per page. Default is 25, max is 100.
        after (Optional[str]): Pagination cursor for the next page. From response['paging']['cursors']['after'].
        before (Optional[str]): Pagination cursor for the previous page. From response['paging']['cursors']['before'].
        effective_status (Optional[List[str]]): Filter ad sets by their effective status.
                                               Options include: 'ACTIVE', 'PAUSED', 'DELETED',
                                               'PENDING_REVIEW', 'DISAPPROVED', 'PREAPPROVED',
                                               'PENDING_BILLING_INFO', 'ARCHIVED', 'WITH_ISSUES'.
        date_format (Optional[str]): Format for date responses. Options:
                                    - 'U': Unix timestamp (seconds since epoch)
                                    - 'Y-m-d H:i:s': MySQL datetime format
                                    - None: ISO 8601 format (default)
    
    Returns:
        Dict: A dictionary containing the requested ad sets. The main results are in the 'data'
              list, and pagination info is in the 'paging' object.
    
    Example:
        ```python
        # Get all active ad sets from a campaign
        adsets = get_adsets_by_campaign(
            campaign_id="23843211234567",
            fields=["name", "effective_status", "daily_budget", "targeting", "optimization_goal"],
            effective_status=["ACTIVE"],
            limit=50
        )
        
        # Get ad sets with specific optimization goals
        conversion_adsets = get_adsets_by_campaign(
            campaign_id="23843211234567",
            fields=["name", "optimization_goal", "billing_event", "bid_amount"],
            filtering=[{
                'field': 'optimization_goal', 
                'operator': 'IN', 
                'value': ['OFFSITE_CONVERSIONS', 'VALUE']
            }]
        )
        
        # Fetch the next page if available using the pagination cursor
        next_page_cursor = adsets.get("paging", {}).get("cursors", {}).get("after")
        if next_page_cursor:
            next_page = get_adsets_by_campaign(
                campaign_id="23843211234567",
                fields=["name", "effective_status", "daily_budget", "targeting"],
                effective_status=["ACTIVE"],
                limit=50,
                after=next_page_cursor
            )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}/adsets"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if filtering:
        params['filtering'] = json.dumps(filtering)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
    
    if effective_status:
        params['effective_status'] = json.dumps(effective_status)
        
    if date_format:
        params['date_format'] = date_format
    
    return _make_graph_api_call(url, params)


# --- Campaign Tools ---
@mcp.tool()
def get_campaign_by_id(
    campaign_id: str, 
    fields: Optional[List[str]] = None,
    date_format: Optional[str] = None
) -> Dict:
    """Retrieves detailed information about a specific Facebook ad campaign by its ID.
    
    This function accesses the Facebook Graph API to retrieve information about a
    single campaign, including details about its objective, status, budget settings,
    and other campaign-level configurations.
    
    Args:
        campaign_id (str): The ID of the campaign to retrieve information for.
        fields (Optional[List[str]]): A list of specific fields to retrieve. If None,
            a default set of fields will be returned. Available fields include:
            - 'id': The campaign's ID
            - 'name': The campaign's name
            - 'account_id': The ID of the ad account this campaign belongs to
            - 'adlabels': Labels applied to the campaign
            - 'bid_strategy': The bid strategy for the campaign. Options include:
                'LOWEST_COST_WITHOUT_CAP', 'LOWEST_COST_WITH_BID_CAP', 'COST_CAP'
            - 'boosted_object_id': The ID of the boosted object
            - 'brand_lift_studies': Brand lift studies associated with this campaign
            - 'budget_rebalance_flag': Whether budget rebalancing is enabled
            - 'budget_remaining': The remaining budget (in cents/smallest currency unit)
            - 'buying_type': The buying type. Options include:
                'AUCTION', 'RESERVED', 'DEPRECATED_REACH_BLOCK'
            - 'can_create_brand_lift_study': Whether a brand lift study can be created
            - 'can_use_spend_cap': Whether a spend cap can be used
            - 'configured_status': Status set by the user. Options include:
                'ACTIVE', 'PAUSED', 'DELETED', 'ARCHIVED'
            - 'created_time': When the campaign was created
            - 'daily_budget': The daily budget (in cents/smallest currency unit)
            - 'effective_status': The effective status accounting for the ad account and other factors.
                Options include: 'ACTIVE', 'PAUSED', 'DELETED', 'PENDING_REVIEW', 'DISAPPROVED',
                'PREAPPROVED', 'PENDING_BILLING_INFO', 'CAMPAIGN_PAUSED', 'ARCHIVED', 'IN_PROCESS',
                'WITH_ISSUES'
            - 'has_secondary_skadnetwork_reporting': Whether secondary SKAdNetwork reporting is available
            - 'is_budget_schedule_enabled': Whether budget scheduling is enabled
            - 'is_skadnetwork_attribution': Whether the campaign uses SKAdNetwork attribution (iOS 14.5+)
            - 'issues_info': Information about issues with this campaign
            - 'last_budget_toggling_time': Last time the budget was toggled
            - 'lifetime_budget': The lifetime budget (in cents/smallest currency unit)
            - 'objective': The campaign's advertising objective. Options include:
                'APP_INSTALLS', 'BRAND_AWARENESS', 'CONVERSIONS', 'EVENT_RESPONSES',
                'LEAD_GENERATION', 'LINK_CLICKS', 'LOCAL_AWARENESS', 'MESSAGES',
                'OFFER_CLAIMS', 'PAGE_LIKES', 'POST_ENGAGEMENT', 'PRODUCT_CATALOG_SALES',
                'REACH', 'STORE_VISITS', 'VIDEO_VIEWS'
            - 'pacing_type': List of pacing types. Options include: 'standard', 'no_pacing'
            - 'primary_attribution': Primary attribution settings
            - 'promoted_object': The object this campaign is promoting
            - 'recommendations': Recommendations for improving this campaign
            - 'smart_promotion_type': Smart promotion type if applicable
            - 'source_campaign': Source campaign if this was created by copying
            - 'source_campaign_id': ID of the source campaign if copied
            - 'special_ad_categories': Array of special ad categories. Options include:
                'EMPLOYMENT', 'HOUSING', 'CREDIT', 'ISSUES_ELECTIONS_POLITICS', 'NONE'
            - 'special_ad_category': Special ad category (deprecated in favor of special_ad_categories)
            - 'spend_cap': The spending cap (in cents/smallest currency unit)
            - 'start_time': When the campaign starts (in ISO 8601 format unless date_format specified)
            - 'status': Deprecated. Use 'configured_status' or 'effective_status' instead
            - 'stop_time': When the campaign stops (in ISO 8601 format unless date_format specified)
            - 'topline_id': Topline ID for this campaign
            - 'updated_time': When this campaign was last updated
        date_format (Optional[str]): Format for date responses. Options:
            - 'U': Unix timestamp (seconds since epoch)
            - 'Y-m-d H:i:s': MySQL datetime format
            - None: ISO 8601 format (default)
    
    Returns:
        Dict: A dictionary containing the requested campaign information.
    
    Example:
        ```python
        # Get basic campaign information
        campaign = get_campaign_by_id(
            campaign_id="23843211234567",
            fields=["name", "objective", "effective_status", "budget_remaining"]
        )
        
        # Get detailed budget information with Unix timestamps
        campaign_budget_details = get_campaign_by_id(
            campaign_id="23843211234567",
            fields=["name", "daily_budget", "lifetime_budget", "start_time", "stop_time"],
            date_format="U"
        )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if date_format:
        params['date_format'] = date_format
    
    return _make_graph_api_call(url, params)

@mcp.tool()
def get_campaigns_by_adaccount(
    act_id: str,
    fields: Optional[List[str]] = None,
    filtering: Optional[List[dict]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    date_preset: Optional[str] = None,
    time_range: Optional[Dict[str, str]] = None,
    updated_since: Optional[int] = None,
    effective_status: Optional[List[str]] = None,
    is_completed: Optional[bool] = None,
    special_ad_categories: Optional[List[str]] = None,
    objective: Optional[List[str]] = None,
    buyer_guarantee_agreement_status: Optional[List[str]] = None,
    date_format: Optional[str] = None,
    include_drafts: Optional[bool] = None
) -> Dict:
    """Retrieves campaigns from a specific Facebook ad account.
    
    This function allows querying all campaigns belonging to a specific ad account with
    various filtering options, pagination, and field selection.
    
    Args:
        act_id (str): The ID of the ad account to retrieve campaigns from, prefixed with 'act_', 
                      e.g., 'act_1234567890'.
        fields (Optional[List[str]]): A list of specific fields to retrieve for each campaign.
                                      If None, a default set of fields will be returned.
                                      See get_campaign_by_id for a comprehensive list of available fields.
        filtering (Optional[List[dict]]): A list of filter objects to apply to the data.
                                         Each object should have 'field', 'operator', and 'value' keys.
                                         Operators include: 'EQUAL', 'NOT_EQUAL', 'GREATER_THAN',
                                         'GREATER_THAN_OR_EQUAL', 'LESS_THAN', 'LESS_THAN_OR_EQUAL',
                                         'IN_RANGE', 'NOT_IN_RANGE', 'CONTAIN', 'NOT_CONTAIN',
                                         'IN', 'NOT_IN', 'EMPTY', 'NOT_EMPTY'.
                                         Example: [{'field': 'daily_budget', 'operator': 'GREATER_THAN', 'value': 1000}]
        limit (Optional[int]): Maximum number of campaigns to return per page. Default is 25, max is 100.
        after (Optional[str]): Pagination cursor for the next page. From response['paging']['cursors']['after'].
        before (Optional[str]): Pagination cursor for the previous page. From response['paging']['cursors']['before'].
        date_preset (Optional[str]): A predefined relative date range for selecting campaigns.
                                    Options include: 'today', 'yesterday', 'this_month', 'last_month', 
                                    'this_quarter', 'maximum', 'last_3d', 'last_7d', 'last_14d', 
                                    'last_28d', 'last_30d', 'last_90d', 'last_week_mon_sun', 
                                    'last_week_sun_sat', 'last_quarter', 'last_year', 
                                    'this_week_mon_today', 'this_week_sun_today', 'this_year'.
        time_range (Optional[Dict[str, str]]): A custom time range with 'since' and 'until' 
                                              dates in 'YYYY-MM-DD' format.
                                              Example: {'since': '2023-01-01', 'until': '2023-01-31'}
        updated_since (Optional[int]): Return campaigns that have been updated since this Unix timestamp.
        effective_status (Optional[List[str]]): Filter campaigns by their effective status. 
                                               Options include: 'ACTIVE', 'PAUSED', 'DELETED', 
                                               'PENDING_REVIEW', 'DISAPPROVED', 'PREAPPROVED', 
                                               'PENDING_BILLING_INFO', 'ARCHIVED', 'WITH_ISSUES'.
        is_completed (Optional[bool]): If True, returns only completed campaigns. If False, returns 
                                      only active campaigns. If None, returns both.
        special_ad_categories (Optional[List[str]]): Filter campaigns by special ad categories.
                                                   Options include: 'EMPLOYMENT', 'HOUSING', 'CREDIT', 
                                                   'ISSUES_ELECTIONS_POLITICS', 'NONE'.
        objective (Optional[List[str]]): Filter campaigns by advertising objective.
                                      Options include: 'APP_INSTALLS', 'BRAND_AWARENESS', 
                                      'CONVERSIONS', 'EVENT_RESPONSES', 'LEAD_GENERATION', 
                                      'LINK_CLICKS', 'LOCAL_AWARENESS', 'MESSAGES', 'OFFER_CLAIMS', 
                                      'PAGE_LIKES', 'POST_ENGAGEMENT', 'PRODUCT_CATALOG_SALES', 
                                      'REACH', 'STORE_VISITS', 'VIDEO_VIEWS'.
        buyer_guarantee_agreement_status (Optional[List[str]]): Filter campaigns by buyer guarantee agreement status.
                                                              Options include: 'APPROVED', 'NOT_APPROVED'.
        date_format (Optional[str]): Format for date responses. Options:
                                    - 'U': Unix timestamp (seconds since epoch)
                                    - 'Y-m-d H:i:s': MySQL datetime format
                                    - None: ISO 8601 format (default)
        include_drafts (Optional[bool]): If True, includes draft campaigns in the results.
    
    Returns:
        Dict: A dictionary containing the requested campaigns. The main results are in the 'data'
              list, and pagination info is in the 'paging' object.
    
    Example:
        ```python
        # Get active campaigns from an ad account
        campaigns = get_campaigns_by_adaccount(
            act_id="act_123456789",
            fields=["name", "objective", "effective_status", "created_time"],
            effective_status=["ACTIVE"],
            limit=50
        )
        
        # Get campaigns with specific objectives
        lead_gen_campaigns = get_campaigns_by_adaccount(
            act_id="act_123456789",
            fields=["name", "objective", "spend_cap", "daily_budget"],
            objective=["LEAD_GENERATION", "CONVERSIONS"],
            date_format="U"
        )
        
        # Get campaigns created in a specific date range
        date_filtered_campaigns = get_campaigns_by_adaccount(
            act_id="act_123456789",
            fields=["name", "created_time", "objective"],
            time_range={"since": "2023-01-01", "until": "2023-01-31"}
        )
        
        # Fetch the next page if available using the pagination cursor
        next_page_cursor = campaigns.get("paging", {}).get("cursors", {}).get("after")
        if next_page_cursor:
            next_page = get_campaigns_by_adaccount(
                act_id="act_123456789",
                fields=["name", "objective", "effective_status", "created_time"],
                effective_status=["ACTIVE"],
                limit=50,
                after=next_page_cursor
            )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/campaigns"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if filtering:
        params['filtering'] = json.dumps(filtering)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
    
    if date_preset:
        params['date_preset'] = date_preset
    
    if time_range:
        params['time_range'] = json.dumps(time_range)
    
    if updated_since:
        params['updated_since'] = updated_since
    
    if effective_status:
        params['effective_status'] = json.dumps(effective_status)
    
    if is_completed is not None:
        params['is_completed'] = is_completed
    
    if special_ad_categories:
        params['special_ad_categories'] = json.dumps(special_ad_categories)
    
    if objective:
        params['objective'] = json.dumps(objective)
    
    if buyer_guarantee_agreement_status:
        params['buyer_guarantee_agreement_status'] = json.dumps(buyer_guarantee_agreement_status)
    
    if date_format:
        params['date_format'] = date_format
    
    if include_drafts is not None:
        params['include_drafts'] = include_drafts
    
    return _make_graph_api_call(url, params)

# --- Activity Tools ---

@mcp.tool()
def get_activities_by_adaccount(
    act_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    time_range: Optional[Dict[str, str]] = None,
    since: Optional[str] = None,
    until: Optional[str] = None
) -> Dict:
    """Retrieves activities for a Facebook ad account.
    
    This function accesses the Facebook Graph API to retrieve information about 
    key updates to an ad account and ad objects associated with it. By default, 
    this API returns one week's data. Information returned includes major account 
    status changes, updates made to budget, campaign, targeting, audiences and more.
    
    Args:
        act_id (str): The ID of the ad account, prefixed with 'act_', e.g., 'act_1234567890'.
        fields (Optional[List[str]]): A list of specific fields to retrieve. If None,
            all available fields will be returned. Available fields include:
            - 'actor_id': ID of the user who made the change
            - 'actor_name': Name of the user who made the change
            - 'application_id': ID of the application used to make the change
            - 'application_name': Name of the application used to make the change
            - 'changed_data': Details about what was changed in JSON format
            - 'date_time_in_timezone': The timestamp in the account's timezone
            - 'event_time': The timestamp of when the event occurred
            - 'event_type': The specific type of change that was made (numeric code)
            - 'extra_data': Additional data related to the change in JSON format
            - 'object_id': ID of the object that was changed (ad, campaign, etc.)
            - 'object_name': Name of the object that was changed
            - 'object_type': Type of object being modified, values include:
              'AD', 'ADSET', 'CAMPAIGN', 'ACCOUNT', 'IMAGE', 'REPORT', etc.
            - 'translated_event_type': Human-readable description of the change made,
              examples include: 'ad created', 'campaign budget updated', 
              'targeting updated', 'ad status changed', etc.
        limit (Optional[int]): Maximum number of activities to return per page.
            Default behavior returns a server-determined number of results.
        after (Optional[str]): Pagination cursor for the next page of results.
            Obtained from the 'paging.cursors.after' field in the previous response.
        before (Optional[str]): Pagination cursor for the previous page of results.
            Obtained from the 'paging.cursors.before' field in the previous response.
        time_range (Optional[Dict[str, str]]): A custom time range with 'since' and 'until'
            dates in 'YYYY-MM-DD' format. Example: {'since': '2023-01-01', 'until': '2023-01-31'}
            This parameter overrides the since/until parameters if both are provided.
        since (Optional[str]): Start date in YYYY-MM-DD format. Defines the beginning 
            of the time range for returned activities. Ignored if 'time_range' is provided.
        until (Optional[str]): End date in YYYY-MM-DD format. Defines the end 
            of the time range for returned activities. Ignored if 'time_range' is provided.
    
    Returns:
        Dict: A dictionary containing the requested activities. The main results are in the 'data'
              list, and pagination info is in the 'paging' object. Each activity object contains
              information about who made the change, what was changed, when it occurred, and
              the specific details of the change.
    
    Example:
        ```python
        # Get recent activities for an ad account with default one week of data
        activities = get_activities_by_adaccount(
            act_id="act_123456789",
            fields=["event_time", "actor_name", "object_type", "translated_event_type"]
        )
        
        # Get all activities from a specific date range
        dated_activities = get_activities_by_adaccount(
            act_id="act_123456789",
            time_range={"since": "2023-01-01", "until": "2023-01-31"},
            fields=["event_time", "actor_name", "object_type", "translated_event_type", "extra_data"]
        )
        
        # Paginate through activity results
        paginated_activities = get_activities_by_adaccount(
            act_id="act_123456789",
            limit=50,
            fields=["event_time", "actor_name", "object_type", "translated_event_type"]
        )
        
        # Get the next page using the cursor from the previous response
        next_page_cursor = paginated_activities.get("paging", {}).get("cursors", {}).get("after")
        if next_page_cursor:
            next_page = get_activities_by_adaccount(
                act_id="act_123456789",
                fields=["event_time", "actor_name", "object_type", "translated_event_type"],
                after=next_page_cursor
            )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/activities"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
    
    # time_range takes precedence over since/until
    if time_range:
        params['time_range'] = json.dumps(time_range)
    else:
        if since:
            params['since'] = since
        if until:
            params['until'] = until
    
    return _make_graph_api_call(url, params)




@mcp.tool()
def get_activities_by_adset(
    adset_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    time_range: Optional[Dict[str, str]] = None,
    since: Optional[str] = None,
    until: Optional[str] = None
) -> Dict:
    """Retrieves activities for a Facebook ad set.
    
    This function accesses the Facebook Graph API to retrieve information about 
    key updates to an ad set. By default, this API returns one week's data. 
    Information returned includes status changes, budget updates, targeting changes, and more.
    
    Args:
        adset_id (str): The ID of the ad set, e.g., '123456789'.
        fields (Optional[List[str]]): A list of specific fields to retrieve. If None,
            all available fields will be returned. Available fields include:
            - 'actor_id': ID of the user who made the change
            - 'actor_name': Name of the user who made the change
            - 'application_id': ID of the application used to make the change
            - 'application_name': Name of the application used to make the change
            - 'changed_data': Details about what was changed in JSON format
            - 'date_time_in_timezone': The timestamp in the account's timezone
            - 'event_time': The timestamp of when the event occurred
            - 'event_type': The specific type of change that was made (numeric code)
            - 'extra_data': Additional data related to the change in JSON format
            - 'object_id': ID of the object that was changed
            - 'object_name': Name of the object that was changed
            - 'object_type': Type of object being modified
            - 'translated_event_type': Human-readable description of the change made,
              examples include: 'adset created', 'adset budget updated', 
              'targeting updated', 'adset status changed', etc.
        limit (Optional[int]): Maximum number of activities to return per page.
            Default behavior returns a server-determined number of results.
        after (Optional[str]): Pagination cursor for the next page of results.
            Obtained from the 'paging.cursors.after' field in the previous response.
        before (Optional[str]): Pagination cursor for the previous page of results.
            Obtained from the 'paging.cursors.before' field in the previous response.
        time_range (Optional[Dict[str, str]]): A custom time range with 'since' and 'until'
            dates in 'YYYY-MM-DD' format. Example: {'since': '2023-01-01', 'until': '2023-01-31'}
            This parameter overrides the since/until parameters if both are provided.
        since (Optional[str]): Start date in YYYY-MM-DD format. Defines the beginning 
            of the time range for returned activities. Ignored if 'time_range' is provided.
        until (Optional[str]): End date in YYYY-MM-DD format. Defines the end 
            of the time range for returned activities. Ignored if 'time_range' is provided.
    
    Returns:
        Dict: A dictionary containing the requested activities. The main results are in the 'data'
              list, and pagination info is in the 'paging' object. Each activity object contains
              information about who made the change, what was changed, when it occurred, and
              the specific details of the change.
    
    Example:
        ```python
        # Get recent activities for an ad set with default one week of data
        activities = get_activities_by_adset(
            adset_id="123456789",
            fields=["event_time", "actor_name", "translated_event_type"]
        )
        
        # Get all activities from a specific date range
        dated_activities = get_activities_by_adset(
            adset_id="123456789",
            time_range={"since": "2023-01-01", "until": "2023-01-31"},
            fields=["event_time", "actor_name", "translated_event_type", "extra_data"]
        )
        
        # Paginate through activity results
        paginated_activities = get_activities_by_adset(
            adset_id="123456789",
            limit=50,
            fields=["event_time", "actor_name", "translated_event_type"]
        )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}/activities"
    params = {
        'access_token': access_token
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    if limit is not None:
        params['limit'] = limit
    
    if after:
        params['after'] = after
    
    if before:
        params['before'] = before
    
    # time_range takes precedence over since/until
    if time_range:
        params['time_range'] = json.dumps(time_range)
    else:
        if since:
            params['since'] = since
        if until:
            params['until'] = until
    
    return _make_graph_api_call(url, params)


# --- Targeting & Audience Search Tools ---

@mcp.tool()
def search_interests(
    query: str,
    limit: Optional[int] = 25,
    locale: Optional[str] = None
) -> Dict:
    """Search for ad interest targeting options by keyword.

    Finds valid interest IDs for use in targeting_spec when creating ad sets.
    
    Args:
        query: Search term to find interests (e.g., 'fitness', 'cooking', 'technology').
        limit: Maximum results to return. Default: 25.
        locale: Locale for results (e.g., 'en_US', 'pt_BR'). Default: API default.
    
    Returns:
        Dict with 'data' list containing interest objects with 'id', 'name', 'audience_size_lower_bound',
        'audience_size_upper_bound', 'path', 'description', 'topic'.
    
    Example:
        ```python
        interests = search_interests(query="fitness", limit=10)
        # Use the returned IDs in targeting_spec: {"interests": [{"id": "123", "name": "Fitness"}]}
        ```
    """
    params = {'q': query}
    if limit:
        params['limit'] = limit
    if locale:
        params['locale'] = locale
    return _make_graph_api_search('adinterest', params)


@mcp.tool()
def search_interest_suggestions(
    interest_list: List[str],
    limit: Optional[int] = 25,
    locale: Optional[str] = None
) -> Dict:
    """Get suggested interests related to given interest IDs.

    Useful for expanding targeting options. Provide existing interest IDs to get related suggestions.
    
    Args:
        interest_list: List of interest IDs to base suggestions on (e.g., ['6003139266461']).
        limit: Maximum results. Default: 25.
        locale: Locale for results (e.g., 'pt_BR').
    
    Returns:
        Dict with 'data' list of suggested interest objects.
    
    Example:
        ```python
        suggestions = search_interest_suggestions(interest_list=["6003139266461"])
        ```
    """
    params = {'interest_list': json.dumps(interest_list)}
    if limit:
        params['limit'] = limit
    if locale:
        params['locale'] = locale
    return _make_graph_api_search('adinterestsuggestion', params)


@mcp.tool()
def search_behaviors(
    locale: Optional[str] = None
) -> Dict:
    """List all available behavior targeting categories.

    Returns behaviors like 'Purchase behavior', 'Digital activities', 'Travel', etc.
    
    Args:
        locale: Locale for results (e.g., 'pt_BR').
    
    Returns:
        Dict with 'data' list of behavior targeting options with 'id', 'name', 'description',
        'audience_size_lower_bound', 'audience_size_upper_bound'.
    """
    params = {'class': 'behaviors'}
    if locale:
        params['locale'] = locale
    return _make_graph_api_search('adTargetingCategory', params)


@mcp.tool()
def search_demographics(
    locale: Optional[str] = None
) -> Dict:
    """List all available demographic targeting categories.

    Returns demographics like 'Life events', 'Income', 'Education', 'Industries', etc.
    
    Args:
        locale: Locale for results (e.g., 'pt_BR').
    
    Returns:
        Dict with 'data' list of demographic targeting options.
    """
    params = {'class': 'demographics'}
    if locale:
        params['locale'] = locale
    return _make_graph_api_search('adTargetingCategory', params)


@mcp.tool()
def search_geolocations(
    query: str,
    location_types: Optional[List[str]] = None,
    country_code: Optional[str] = None,
    region_id: Optional[int] = None,
    limit: Optional[int] = 25,
    locale: Optional[str] = None
) -> Dict:
    """Search for geographic locations for ad targeting.

    Find countries, cities, regions, zip codes, geo markets, and electoral districts.
    
    Args:
        query: Search term (e.g., 'Brazil', 'São Paulo', 'New York').
        location_types: Filter by type. Options: 'country', 'country_group', 'region',
            'city', 'zip', 'geo_market', 'electoral_district'. Default: all types.
        country_code: Filter results to a specific country (e.g., 'BR', 'US').
        region_id: Filter results to a specific region ID.
        limit: Maximum results. Default: 25.
        locale: Locale for results (e.g., 'pt_BR').
    
    Returns:
        Dict with 'data' list of location objects with 'key', 'name', 'type',
        'country_code', 'supports_region', 'supports_city'.
    
    Example:
        ```python
        # Search for cities in Brazil
        cities = search_geolocations(
            query="São Paulo",
            location_types=["city"],
            country_code="BR"
        )
        ```
    """
    params = {'q': query}
    if location_types:
        params['location_types'] = json.dumps(location_types)
    if country_code:
        params['country_code'] = country_code
    if region_id:
        params['region_id'] = region_id
    if limit:
        params['limit'] = limit
    if locale:
        params['locale'] = locale
    return _make_graph_api_search('adgeolocation', params)


@mcp.tool()
def validate_targeting(
    act_id: str,
    targeting_spec: Dict
) -> Dict:
    """Validate if a targeting specification is valid for an ad account.

    Use this before creating an ad set to ensure the targeting_spec will be accepted.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        targeting_spec: The targeting specification dict to validate.
    
    Returns:
        Dict with validation results. Returns the validated targeting if valid,
        or error details if invalid.
    
    Example:
        ```python
        result = validate_targeting(
            act_id="act_123456789",
            targeting_spec={
                "geo_locations": {"countries": ["BR"]},
                "interests": [{"id": "6003139266461", "name": "Fitness"}],
                "age_min": 18, "age_max": 65
            }
        )
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/targetingvalidation"
    params = {
        'access_token': access_token,
        'targeting_spec': json.dumps(targeting_spec)
    }
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_reach_estimate(
    act_id: str,
    targeting_spec: Dict,
    optimization_goal: Optional[str] = None
) -> Dict:
    """Estimate audience size for a given targeting specification.

    Returns estimated reach (lower/upper bounds) before creating an ad set.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        targeting_spec: The targeting specification dict.
        optimization_goal: Optional optimization goal (e.g., 'REACH', 'LINK_CLICKS').
    
    Returns:
        Dict with 'data' containing 'users_lower_bound' and 'users_upper_bound'.
    
    Example:
        ```python
        estimate = get_reach_estimate(
            act_id="act_123456789",
            targeting_spec={
                "geo_locations": {"countries": ["BR"]},
                "age_min": 25, "age_max": 45
            }
        )
        print(f"Estimated reach: {estimate['data']['users_lower_bound']} - {estimate['data']['users_upper_bound']}")
        ```
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/reachestimate"
    params = {
        'access_token': access_token,
        'targeting_spec': json.dumps(targeting_spec)
    }
    if optimization_goal:
        params['optimization_goal'] = optimization_goal
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_delivery_estimate(
    act_id: str,
    targeting_spec: Dict,
    optimization_goal: str,
    daily_budget: Optional[int] = None,
    lifetime_budget: Optional[int] = None
) -> Dict:
    """Get delivery estimates (CPA/CPM/impressions) for a targeting spec and budget.

    Predicts performance metrics before launching a campaign.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        targeting_spec: The targeting specification dict.
        optimization_goal: Goal to optimize for (e.g., 'LINK_CLICKS', 'CONVERSIONS',
            'REACH', 'IMPRESSIONS', 'OFFSITE_CONVERSIONS').
        daily_budget: Daily budget in cents (e.g., 5000 = $50.00). Provide either this or lifetime_budget.
        lifetime_budget: Lifetime budget in cents. Provide either this or daily_budget.
    
    Returns:
        Dict with delivery estimates including estimated daily reach, estimated actions, etc.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/delivery_estimate"
    params = {
        'access_token': access_token,
        'targeting_spec': json.dumps(targeting_spec),
        'optimization_goal': optimization_goal
    }
    if daily_budget:
        params['daily_budget'] = daily_budget
    if lifetime_budget:
        params['lifetime_budget'] = lifetime_budget
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_targeting_description(
    act_id: str,
    targeting_spec: Dict
) -> Dict:
    """Convert a targeting specification into human-readable text.

    Generates a description like "People aged 25-45 in Brazil who like Fitness".
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        targeting_spec: The targeting specification dict to describe.
    
    Returns:
        Dict with 'targetingsentencelines' containing readable text per targeting dimension.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/targetingsentencelines"
    params = {
        'access_token': access_token,
        'targeting_spec': json.dumps(targeting_spec)
    }
    return _make_graph_api_call(url, params)


@mcp.tool()
def list_custom_audiences(
    act_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    business_id: Optional[str] = None
) -> Dict:
    """List custom audiences (retargeting audiences) for an ad account.

    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        fields: Fields to retrieve. Common: 'id', 'name', 'subtype', 'description',
            'approximate_count_lower_bound', 'approximate_count_upper_bound',
            'time_created', 'time_updated', 'delivery_status', 'operation_status'.
        limit: Max results per page. Default: 25.
        after: Pagination cursor for next page.
        before: Pagination cursor for previous page.
        business_id: Optional business ID for filtering.
    
    Returns:
        Dict with 'data' list of custom audience objects and 'paging' info.
    """
    return _fetch_edge(
        parent_id=act_id,
        edge_name='customaudiences',
        fields=fields,
        limit=limit,
        after=after,
        before=before,
        business_id=business_id
    )


@mcp.tool()
def list_lookalike_audiences(
    act_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None
) -> Dict:
    """List lookalike audiences for an ad account.

    Filters custom audiences to show only LOOKALIKE subtypes.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        fields: Fields to retrieve. Common: 'id', 'name', 'approximate_count_lower_bound',
            'approximate_count_upper_bound', 'lookalike_spec', 'delivery_status'.
        limit: Max results per page. Default: 25.
        after: Pagination cursor for next page.
        before: Pagination cursor for previous page.
    
    Returns:
        Dict with 'data' list of lookalike audience objects.
    """
    filtering = [{'field': 'subtype', 'operator': 'EQUAL', 'value': 'LOOKALIKE'}]
    return _fetch_edge(
        parent_id=act_id,
        edge_name='customaudiences',
        fields=fields,
        filtering=filtering,
        limit=limit,
        after=after,
        before=before
    )


# --- Campaign Management Tools (Write) ---

@mcp.tool()
def create_campaign(
    act_id: str,
    name: str,
    objective: str,
    status: str = 'PAUSED',
    special_ad_categories: Optional[List[str]] = None,
    daily_budget: Optional[int] = None,
    lifetime_budget: Optional[int] = None,
    bid_strategy: Optional[str] = None,
    buying_type: Optional[str] = None,
    start_time: Optional[str] = None,
    stop_time: Optional[str] = None,
    spend_cap: Optional[int] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Create a new Facebook ad campaign.

    Creates a campaign with the specified objective and settings.
    Campaign is created PAUSED by default for safety.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        name: Campaign name.
        objective: Campaign objective. Options: 'OUTCOME_AWARENESS', 'OUTCOME_ENGAGEMENT',
            'OUTCOME_LEADS', 'OUTCOME_SALES', 'OUTCOME_TRAFFIC', 'OUTCOME_APP_PROMOTION'.
        status: Initial status. Default: 'PAUSED'. Options: 'ACTIVE', 'PAUSED'.
        special_ad_categories: Required list. Options: 'EMPLOYMENT', 'HOUSING', 'CREDIT',
            'ISSUES_ELECTIONS_POLITICS'. Use ['NONE'] if none apply.
        daily_budget: Daily budget in cents (e.g., 5000 = $50.00).
        lifetime_budget: Lifetime budget in cents. Cannot use with daily_budget.
        bid_strategy: Bid strategy. Options: 'LOWEST_COST_WITHOUT_CAP',
            'LOWEST_COST_WITH_BID_CAP', 'COST_CAP'.
        buying_type: Buying type. Options: 'AUCTION' (default), 'RESERVED'.
        start_time: Start time in ISO 8601 format.
        stop_time: Stop time in ISO 8601 format (required for lifetime_budget).
        spend_cap: Spend cap in cents.
    
    Returns:
        Dict with 'id' of the created campaign.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/campaigns"
    data = {
        'access_token': access_token,
        'name': name,
        'objective': objective,
        'status': status,
        'special_ad_categories': json.dumps(special_ad_categories or ['NONE'])
    }
    if daily_budget is not None:
        data['daily_budget'] = daily_budget
    if lifetime_budget is not None:
        data['lifetime_budget'] = lifetime_budget
    if bid_strategy:
        data['bid_strategy'] = bid_strategy
    if buying_type:
        data['buying_type'] = buying_type
    if start_time:
        data['start_time'] = start_time
    if stop_time:
        data['stop_time'] = stop_time
    if spend_cap is not None:
        data['spend_cap'] = spend_cap
    return _make_graph_api_post(url, data)


@mcp.tool()
def update_campaign(
    campaign_id: str,
    name: Optional[str] = None,
    status: Optional[str] = None,
    daily_budget: Optional[int] = None,
    lifetime_budget: Optional[int] = None,
    bid_strategy: Optional[str] = None,
    spend_cap: Optional[int] = None,
    start_time: Optional[str] = None,
    stop_time: Optional[str] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Update an existing Facebook ad campaign.

    Use this to change campaign name, status (pause/activate), budget, etc.
    Only provided parameters will be updated.
    
    Args:
        campaign_id: Campaign ID to update.
        name: New campaign name.
        status: New status. Options: 'ACTIVE', 'PAUSED', 'DELETED', 'ARCHIVED'.
        daily_budget: New daily budget in cents.
        lifetime_budget: New lifetime budget in cents.
        bid_strategy: New bid strategy.
        spend_cap: New spend cap in cents.
        start_time: New start time in ISO 8601 format.
        stop_time: New stop time in ISO 8601 format.
    
    Returns:
        Dict with 'success': true if updated.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}"
    data = {'access_token': access_token}
    if name:
        data['name'] = name
    if status:
        data['status'] = status
    if daily_budget is not None:
        data['daily_budget'] = daily_budget
    if lifetime_budget is not None:
        data['lifetime_budget'] = lifetime_budget
    if bid_strategy:
        data['bid_strategy'] = bid_strategy
    if spend_cap is not None:
        data['spend_cap'] = spend_cap
    if start_time:
        data['start_time'] = start_time
    if stop_time:
        data['stop_time'] = stop_time
    return _make_graph_api_post(url, data)


@mcp.tool()
def create_adset(
    act_id: str,
    name: str,
    campaign_id: str,
    optimization_goal: str,
    billing_event: str,
    targeting: Dict,
    status: str = 'PAUSED',
    daily_budget: Optional[int] = None,
    lifetime_budget: Optional[int] = None,
    bid_amount: Optional[int] = None,
    bid_strategy: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    promoted_object: Optional[Dict] = None,
    destination_type: Optional[str] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Create a new Facebook ad set.

    Creates an ad set with targeting, budget, and optimization settings.
    Created PAUSED by default for safety.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        name: Ad set name.
        campaign_id: Parent campaign ID.
        optimization_goal: Goal to optimize. Options: 'REACH', 'IMPRESSIONS', 'LINK_CLICKS',
            'OFFSITE_CONVERSIONS', 'LEAD_GENERATION', 'APP_INSTALLS', 'VALUE', 'THRUPLAY',
            'LANDING_PAGE_VIEWS', 'POST_ENGAGEMENT', 'PAGE_LIKES', 'QUALITY_LEAD'.
        billing_event: When to bill. Options: 'IMPRESSIONS', 'LINK_CLICKS', 'THRUPLAY'.
        targeting: Targeting specification dict. Must include at least geo_locations.
            Example: {"geo_locations": {"countries": ["BR"]}, "age_min": 18, "age_max": 65}
        status: Initial status. Default: 'PAUSED'.
        daily_budget: Daily budget in cents. Either this or lifetime_budget is required.
        lifetime_budget: Lifetime budget in cents.
        bid_amount: Bid amount in cents (for BID_CAP strategy).
        bid_strategy: Bid strategy override.
        start_time: Start time in ISO 8601 format.
        end_time: End time in ISO 8601 (required for lifetime_budget).
        promoted_object: Object to promote (e.g., {"page_id": "123"} or {"pixel_id": "456", "custom_event_type": "PURCHASE"}).
        destination_type: Destination type (e.g., 'WEBSITE', 'APP', 'MESSENGER').
    
    Returns:
        Dict with 'id' of the created ad set.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/adsets"
    data = {
        'access_token': access_token,
        'name': name,
        'campaign_id': campaign_id,
        'optimization_goal': optimization_goal,
        'billing_event': billing_event,
        'targeting': json.dumps(targeting),
        'status': status
    }
    if daily_budget is not None:
        data['daily_budget'] = daily_budget
    if lifetime_budget is not None:
        data['lifetime_budget'] = lifetime_budget
    if bid_amount is not None:
        data['bid_amount'] = bid_amount
    if bid_strategy:
        data['bid_strategy'] = bid_strategy
    if start_time:
        data['start_time'] = start_time
    if end_time:
        data['end_time'] = end_time
    if promoted_object:
        data['promoted_object'] = json.dumps(promoted_object)
    if destination_type:
        data['destination_type'] = destination_type
    return _make_graph_api_post(url, data)


@mcp.tool()
def update_adset(
    adset_id: str,
    name: Optional[str] = None,
    status: Optional[str] = None,
    daily_budget: Optional[int] = None,
    lifetime_budget: Optional[int] = None,
    targeting: Optional[Dict] = None,
    bid_amount: Optional[int] = None,
    bid_strategy: Optional[str] = None,
    optimization_goal: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Update an existing Facebook ad set.

    Use this to change targeting, budget, status, schedule, etc.
    Only provided parameters will be updated.
    
    Args:
        adset_id: Ad set ID.
        name: New name.
        status: New status. Options: 'ACTIVE', 'PAUSED', 'DELETED', 'ARCHIVED'.
        daily_budget: New daily budget in cents.
        lifetime_budget: New lifetime budget in cents.
        targeting: New targeting spec dict.
        bid_amount: New bid amount in cents.
        bid_strategy: New bid strategy.
        optimization_goal: New optimization goal.
        start_time: New start time in ISO 8601.
        end_time: New end time in ISO 8601.
    
    Returns:
        Dict with 'success': true if updated.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}"
    data = {'access_token': access_token}
    if name:
        data['name'] = name
    if status:
        data['status'] = status
    if daily_budget is not None:
        data['daily_budget'] = daily_budget
    if lifetime_budget is not None:
        data['lifetime_budget'] = lifetime_budget
    if targeting:
        data['targeting'] = json.dumps(targeting)
    if bid_amount is not None:
        data['bid_amount'] = bid_amount
    if bid_strategy:
        data['bid_strategy'] = bid_strategy
    if optimization_goal:
        data['optimization_goal'] = optimization_goal
    if start_time:
        data['start_time'] = start_time
    if end_time:
        data['end_time'] = end_time
    return _make_graph_api_post(url, data)


@mcp.tool()
def create_ad(
    act_id: str,
    name: str,
    adset_id: str,
    creative: Dict,
    status: str = 'PAUSED',
    tracking_specs: Optional[List[Dict]] = None,
    conversion_domain: Optional[str] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Create a new Facebook ad.

    Creates an ad linking a creative to an ad set. Created PAUSED by default.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        name: Ad name.
        adset_id: Parent ad set ID.
        creative: Creative specification. Either reference an existing creative with
            {"creative_id": "123"} or provide inline spec with object_story_spec.
        status: Initial status. Default: 'PAUSED'.
        tracking_specs: Tracking specifications for conversions.
        conversion_domain: Domain for conversion tracking.
    
    Returns:
        Dict with 'id' of the created ad.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/ads"
    data = {
        'access_token': access_token,
        'name': name,
        'adset_id': adset_id,
        'creative': json.dumps(creative),
        'status': status
    }
    if tracking_specs:
        data['tracking_specs'] = json.dumps(tracking_specs)
    if conversion_domain:
        data['conversion_domain'] = conversion_domain
    return _make_graph_api_post(url, data)


@mcp.tool()
def update_ad(
    ad_id: str,
    name: Optional[str] = None,
    status: Optional[str] = None,
    creative: Optional[Dict] = None,
    tracking_specs: Optional[List[Dict]] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Update an existing Facebook ad.

    Use this to change ad name, status (pause/activate), or creative.
    Only provided parameters will be updated.
    
    Args:
        ad_id: Ad ID to update.
        name: New ad name.
        status: New status. Options: 'ACTIVE', 'PAUSED', 'DELETED', 'ARCHIVED'.
        creative: New creative spec (e.g., {"creative_id": "123"}).
        tracking_specs: New tracking specifications.
    
    Returns:
        Dict with 'success': true if updated.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}"
    data = {'access_token': access_token}
    if name:
        data['name'] = name
    if status:
        data['status'] = status
    if creative:
        data['creative'] = json.dumps(creative)
    if tracking_specs:
        data['tracking_specs'] = json.dumps(tracking_specs)
    return _make_graph_api_post(url, data)


@mcp.tool()
def create_ad_creative(
    act_id: str,
    name: str,
    object_story_spec: Optional[Dict] = None,
    asset_feed_spec: Optional[Dict] = None,
    url_tags: Optional[str] = None,
    call_to_action_type: Optional[str] = None,
    image_hash: Optional[str] = None,
    image_url: Optional[str] = None,
    video_id: Optional[str] = None,
    link_url: Optional[str] = None,
    title: Optional[str] = None,
    body: Optional[str] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Create a new Facebook ad creative.

    Creates a creative with image/video, text, and CTA. Use object_story_spec for
    feed ads or asset_feed_spec for dynamic creative.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        name: Creative name.
        object_story_spec: Page post spec for the creative. Example:
            {"page_id": "123", "link_data": {"link": "https://example.com",
            "message": "Check this out!", "image_hash": "abc123"}}
        asset_feed_spec: For dynamic creative optimization with multiple assets.
        url_tags: UTM parameters to append to URLs (e.g., 'utm_source=facebook').
        call_to_action_type: CTA button type. Options: 'LEARN_MORE', 'SHOP_NOW',
            'SIGN_UP', 'BOOK_TRAVEL', 'CONTACT_US', 'DOWNLOAD', 'GET_OFFER',
            'GET_QUOTE', 'SUBSCRIBE', 'WATCH_MORE', 'APPLY_NOW'.
        image_hash: Hash of previously uploaded image.
        image_url: URL of image to use.
        video_id: ID of previously uploaded video.
        link_url: Destination URL.
        title: Ad headline text.
        body: Ad body text.
    
    Returns:
        Dict with 'id' of the created creative.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/adcreatives"
    data = {
        'access_token': access_token,
        'name': name
    }
    if object_story_spec:
        data['object_story_spec'] = json.dumps(object_story_spec)
    if asset_feed_spec:
        data['asset_feed_spec'] = json.dumps(asset_feed_spec)
    if url_tags:
        data['url_tags'] = url_tags
    if call_to_action_type:
        data['call_to_action_type'] = call_to_action_type
    if image_hash:
        data['image_hash'] = image_hash
    if image_url:
        data['image_url'] = image_url
    if video_id:
        data['video_id'] = video_id
    if link_url:
        data['link_url'] = link_url
    if title:
        data['title'] = title
    if body:
        data['body'] = body
    return _make_graph_api_post(url, data)


@mcp.tool()
def delete_object(
    object_id: str
) -> Dict:
    """⚠️ WRITE OPERATION — Delete/archive a Facebook ads object.

    Archives campaigns, ad sets, ads, or creatives. This is a soft delete (archive).
    
    Args:
        object_id: ID of the object to delete (campaign, ad set, ad, or creative ID).
    
    Returns:
        Dict with 'success': true if deleted/archived.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{object_id}"
    params = {'access_token': access_token}
    return _make_graph_api_delete(url, params)


# --- Media Tools ---

@mcp.tool()
def upload_ad_image(
    act_id: str,
    image_url: str,
    name: Optional[str] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Upload an image to the ad account library via URL.

    Uploads an image from a URL to be used in ad creatives. Returns the image hash
    needed for creating creatives.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        image_url: Public URL of the image to upload.
        name: Optional name for the image in the library.
    
    Returns:
        Dict with image details including 'hash', 'url', 'width', 'height'.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/adimages"
    data = {
        'access_token': access_token,
        'url': image_url
    }
    if name:
        data['name'] = name
    return _make_graph_api_post(url, data)


@mcp.tool()
def list_ad_images(
    act_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
    hashes: Optional[List[str]] = None
) -> Dict:
    """List images in an ad account's image library.

    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        fields: Fields to retrieve. Common: 'id', 'hash', 'name', 'url',
            'width', 'height', 'created_time', 'status', 'permalink_url'.
        limit: Max results per page. Default: 25.
        after: Pagination cursor.
        before: Pagination cursor.
        hashes: Filter by specific image hashes.
    
    Returns:
        Dict with 'data' list of image objects.
    """
    params = {}
    if hashes:
        params['hashes'] = json.dumps(hashes)
    return _fetch_edge(
        parent_id=act_id,
        edge_name='adimages',
        fields=fields,
        limit=limit,
        after=after,
        before=before,
        **params
    )


@mcp.tool()
def upload_ad_video(
    act_id: str,
    file_url: str,
    name: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Upload a video to the ad account library via URL.

    Uploads a video from a URL to be used in ad creatives.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        file_url: Public URL of the video to upload.
        name: Name for the video in the library.
        title: Video title.
        description: Video description.
    
    Returns:
        Dict with video details including 'id'.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/advideos"
    data = {
        'access_token': access_token,
        'file_url': file_url
    }
    if name:
        data['name'] = name
    if title:
        data['title'] = title
    if description:
        data['description'] = description
    return _make_graph_api_post(url, data)


@mcp.tool()
def list_ad_videos(
    act_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = 25,
    after: Optional[str] = None,
    before: Optional[str] = None
) -> Dict:
    """List videos in an ad account's video library.

    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        fields: Fields to retrieve. Common: 'id', 'title', 'description',
            'source', 'picture', 'created_time', 'updated_time', 'length'.
        limit: Max results per page. Default: 25.
        after: Pagination cursor.
        before: Pagination cursor.
    
    Returns:
        Dict with 'data' list of video objects.
    """
    return _fetch_edge(
        parent_id=act_id,
        edge_name='advideos',
        fields=fields,
        limit=limit,
        after=after,
        before=before
    )


# --- Ad Preview Tools ---

@mcp.tool()
def get_ad_preview(
    creative_id: str,
    ad_format: str = 'DESKTOP_FEED_STANDARD'
) -> Dict:
    """Get a preview of how an ad creative will look.

    Generates an HTML preview of the ad creative in the specified format.
    
    Args:
        creative_id: The ad creative ID to preview.
        ad_format: Preview format. Options:
            'DESKTOP_FEED_STANDARD', 'MOBILE_FEED_STANDARD', 'MOBILE_FEED_BASIC',
            'RIGHT_COLUMN_STANDARD', 'INSTAGRAM_STANDARD', 'INSTAGRAM_STORY',
            'MARKETPLACE_MOBILE', 'AUDIENCE_NETWORK_OUTSTREAM_VIDEO',
            'INSTANT_ARTICLE_STANDARD', 'MESSENGER_MOBILE_INBOX_MEDIA'.
    
    Returns:
        Dict with 'data' containing preview HTML in 'body' field.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{creative_id}/previews"
    params = {
        'access_token': access_token,
        'ad_format': ad_format
    }
    return _make_graph_api_call(url, params)


# --- Audience Management Tools ---

@mcp.tool()
def create_custom_audience(
    act_id: str,
    name: str,
    subtype: str = 'CUSTOM',
    description: Optional[str] = None,
    customer_file_source: Optional[str] = None
) -> Dict:
    """⚠️ WRITE OPERATION — Create a custom audience for retargeting.

    Creates a blank custom audience that can be populated with users later.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        name: Audience name.
        subtype: Audience subtype. Options: 'CUSTOM', 'WEBSITE', 'APP', 'OFFLINE_CONVERSION',
            'ENGAGEMENT', 'VIDEO'. Default: 'CUSTOM'.
        description: Description of the audience.
        customer_file_source: Source of customer data. Options: 'USER_PROVIDED_ONLY',
            'PARTNER_PROVIDED_ONLY', 'BOTH_USER_AND_PARTNER_PROVIDED'.
    
    Returns:
        Dict with 'id' of the created audience.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/customaudiences"
    data = {
        'access_token': access_token,
        'name': name,
        'subtype': subtype
    }
    if description:
        data['description'] = description
    if customer_file_source:
        data['customer_file_source'] = customer_file_source
    return _make_graph_api_post(url, data)


@mcp.tool()
def update_custom_audience_users(
    audience_id: str,
    schema: List[str],
    data_list: List[List[str]],
    action: str = 'add'
) -> Dict:
    """⚠️ WRITE OPERATION — Add or remove users from a custom audience.

    Adds/removes hashed user data to/from a custom audience.
    Data must be SHA256 hashed before sending (except for phone numbers and emails
    which should be lowercase and trimmed then hashed).
    
    Args:
        audience_id: Custom audience ID.
        schema: Schema of the data columns. Options: 'EMAIL', 'PHONE', 'FN' (first name),
            'LN' (last name), 'ZIP', 'CT' (city), 'ST' (state), 'COUNTRY', 'DOBY' (birth year),
            'DOBM' (birth month), 'DOBD' (birth day), 'GEN' (gender), 'EXTERN_ID'.
        data_list: List of user records. Each record is a list matching the schema.
            All PII values must be SHA256 hashed.
        action: 'add' to add users, 'remove' to remove users. Default: 'add'.
    
    Returns:
        Dict with 'audience_id' and 'num_received', 'num_invalid_entries'.
    """
    access_token = _get_fb_access_token()
    endpoint = 'users' if action == 'add' else 'users'
    url = f"{FB_GRAPH_URL}/{audience_id}/{endpoint}"
    payload = {
        'schema': schema,
        'data': data_list
    }
    data = {
        'access_token': access_token,
        'payload': json.dumps(payload)
    }
    if action == 'remove':
        # For removal, we use DELETE method conceptually but Meta uses POST with session
        data['method'] = 'DELETE'
    return _make_graph_api_post(url, data)


@mcp.tool()
def create_lookalike_audience(
    act_id: str,
    name: str,
    origin_audience_id: str,
    lookalike_spec: Dict
) -> Dict:
    """⚠️ WRITE OPERATION — Create a lookalike audience based on a source audience.

    Creates a new audience of people similar to your existing custom audience.
    
    Args:
        act_id: Ad account ID (e.g., 'act_1234567890').
        name: Name for the lookalike audience.
        origin_audience_id: Source custom audience ID to base the lookalike on.
        lookalike_spec: Lookalike configuration. Example:
            {"type": "similarity", "country": "BR", "ratio": 0.01}
            or {"type": "similarity", "country": "BR", "starting_ratio": 0.0, "ratio": 0.02}
            ratio values: 0.01 = 1% (most similar), 0.10 = 10% (broader reach).
    
    Returns:
        Dict with 'id' of the created lookalike audience.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/customaudiences"
    data = {
        'access_token': access_token,
        'name': name,
        'subtype': 'LOOKALIKE',
        'origin_audience_id': origin_audience_id,
        'lookalike_spec': json.dumps(lookalike_spec)
    }
    return _make_graph_api_post(url, data)


@mcp.tool()
def delete_audience(
    audience_id: str
) -> Dict:
    """⚠️ WRITE OPERATION — Delete a custom or lookalike audience.

    Permanently removes the audience. This action cannot be undone.
    
    Args:
        audience_id: ID of the custom or lookalike audience to delete.
    
    Returns:
        Dict with 'success': true if deleted.
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{audience_id}"
    params = {'access_token': access_token}
    return _make_graph_api_delete(url, params)


if __name__ == "__main__":
    _get_fb_access_token()
    mcp.run(transport='stdio')