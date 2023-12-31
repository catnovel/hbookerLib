# HbookerAPI Documentation

## Overview

`HbookerAPI` is a Python class designed to interact with the Hbooker application's API. It provides methods to perform
various actions such as logging in, fetching shelf lists, retrieving chapter updates, and more. The class uses a common
set of parameters for requests and handles the encryption and decryption of data as required by the Hbooker API.

## Initialization

Upon instantiation, the `HbookerAPI` class initializes with no account or login token. It sets up common parameters that
will be used in every API call, including the application version and a unique device token.

```python
class HbookerAPI:
    def __init__(self):
        self.account = None
        self.login_token = None
        self.util = util.Util()
        self.common_params = {'app_version': '2.9.290', 'device_token': 'ciweimao_'}
```

## Methods

### `set_common_params(account, login_token)`

Sets the account and login token parameters to be included in all subsequent API calls.

### `post(api_url, data=None)`

Makes a POST request to the specified `api_url` using the provided `data` along with the common parameters. It decrypts
the response received from the server.

### `login(login_name, passwd)`

Performs a login action using the user's login name and password.

### `get_shelf_list()`

Fetches the user's shelf list from the API.

### `get_shelf_book_list(shelf_id, last_mod_time='0', direction='prev')`

Retrieves the list of books on a specific shelf identified by `shelf_id`.

### `get_division_list(book_id)`

Gets the division list for a given book by `book_id`.

### `get_updated_chapter_by_division_new(book_id: str)`

Obtains the updated chapters by division for the book identified by `book_id`.

### `get_chapter_update(division_id, last_update_time='0')`

Retrieves the chapter updates for a specific division, optionally using `last_update_time` to filter recent updates.

### `get_info_by_id(book_id)`

Gets information for a book by its `book_id`.

### `get_chapter_command(chapter_id)`

Gets command information for a specific chapter identified by `chapter_id`.

### `get_cpt_ifm(chapter_id, chapter_command)`

Fetches information about a chapter using `chapter_id` and a `chapter_command`.

### `get_check_in_records()`

Retrieves the user's check-in records.

### `do_check_in()`

Performs a check-in action for the user.

### `get_version()`

Obtains the current version of the application from the API.

## Usage

Before using the `HbookerAPI` class, it's necessary to import the required modules and set up the proper environment.
After instantiation, the user must log in to authenticate and then can use the various methods to interact with the API.

```python
# Example usage
hbooker_api = HbookerAPI()
login_response = hbooker_api.login('your_username', 'your_password')

if login_response['code'] == 0:
    # Login successful, set common parameters
    hbooker_api.set_common_params(login_response['account'], login_response['login_token'])

    # Fetch shelf list
    shelf_list = hbooker_api.get_shelf_list()
    print(shelf_list)
```

## Error Handling

The `post` method includes a try-except block to handle any exceptions that may occur during the request. It prints the
error message to the console.

```python
try:
    return json.loads(self.util.decrypt(self.util.post(UrlConstants.WEB_SITE + api_point, data=data)))
except Exception as error:
    print("post error:", error)
```

---
