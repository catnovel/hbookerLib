# HbookerAPI Python Client

## Overview

The `HbookerAPI` class is a Python client for interacting with a specific API, which seems to be related to a book
reading or publishing service. It provides methods to perform actions such as retrieving user information, logging in,
signing up, managing bookshelves, fetching book details, and handling chapters and check-in records.

## Installation

Before you can use the `HbookerAPI` class, make sure you have Python installed on your system. Then, you'll need to
install the necessary dependencies, which may include a custom `client` module and other libraries used by this class.
Since the exact dependencies are not listed, you will need to review the code and install any imports that are
referenced.

```bash
pip install <https://github.com/catnovel/hbookerLib>
```
 
## Usage

To use the `HbookerAPI` class, you must first create an instance of the class, optionally providing an account and login
token. If you provide these credentials, you can also choose to verify the token immediately.

```python
from hbooker import HbookerAPI

api_client = HbookerAPI(account='your_account', login_token='your_token', verify_token=True)
```

### Methods

Below is a list of available methods along with their descriptions:

#### `__init__(self, account=None, login_token=None, verify_token=False)`

Initialize the API client with optional account and login token. If `verify_token` is `True`, it will immediately
validate the provided credentials.

#### `verify_token(self)`

Verify the provided login token.

#### `get_my_info(self)`

Retrieve the current user's information.

#### `login(self, login_name, passwd)`

*(Deprecated)* Login with a username and password. This method is invalid due to additional verification requirements.

#### `signup_use_geetest(self, login_name)`

Sign up using the Geetest verification with a login name.

#### `signup_first_register(self, login_name)`

Perform the first step of registration for a new user.

#### `login_new(self, login_name, passwd, geetest_validate, geetest_challenge)`

Login with Geetest verification data.

#### `get_shelf_list(self)`

Retrieve the list of shelves.

#### `get_shelf_book_list(self, shelf_id, last_mod_time='0', direction='prev')`

*(Deprecated)* Get a list of books from a specific shelf.

#### `get_shelf_book_list_new(self, shelf_id)`

Get a list of books from a specific shelf using the new interface.

#### `get_bookshelf(self)`

Retrieve the entire bookshelf and list of books.

#### `get_division_list(self, book_id)`

*(Deprecated)* Get a list of divisions for a given book.

#### `get_chapter_update(self, division_id)`

*(Deprecated)* Get updates for chapters within a division.

#### `get_updated_chapter_by_division_new(self, book_id)`

Get updated chapters for a given book using the new interface.

#### `get_info_by_id(self, book_id)`

Retrieve information for a book by its ID.

#### `get_chapter_command(self, chapter_id)`

Get the command needed to fetch a specific chapter's content.

#### `get_cpt_ifm(self, chapter_id, command)`

Get chapter information including the command needed to decrypt content.

#### `get_chapter_content(self, chapter_id)`

Retrieve and decrypt the content of a chapter.

#### `get_check_in_records(self)`

Get check-in records for the current user.

#### `do_check_in(self)`

Perform a check-in action.

#### `get_version(self)`

Retrieve the current version of the service.

#### `auto_req_v2(self, android_id=None)`

Automatically send a request with optional Android ID.

## Examples

### Fetching User Info

```python
user_info = api_client.get_my_info()
if user_info.get('code') == '100000':
    print(user_info)
else:
    print("Failed to fetch user info.")
```

### Checking In

```python
check_in_response = api_client.do_check_in()
if check_in_response.get('code') == '100000':
    print("Check-in successful!")
else:
    print("Check-in failed.")
```

## Contributing

Contributions to this client are welcome. Please make sure to update tests as appropriate.

## License

Specify the license under which this code is made available, such as MIT or GPL.

---
