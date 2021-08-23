import requests
from assertpy import assert_that

BASE_URL = 'http://127.0.0.1:5000'
GET_WISHLIST_URL = BASE_URL + "/user/{uid}/book"
DELETE_BOOK_URL = BASE_URL + "/user/{uid}/book/{bid}"
EMPTY_WISHLIST_URL = BASE_URL + "/user/{uid}/book"
ADD_WISHLIST_URL = BASE_URL + "/user/{uid}/book/{bid}"


def test_get_wishlist_returs_results() :
    USER = 1

    response = requests.get(GET_WISHLIST_URL.format(uid=USER))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response_json).is_not_empty()


def test_get_wishlist_returs_empty_results_when_wishlist_empty() :
    USER = 2

    response = requests.get(GET_WISHLIST_URL.format(uid=USER))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response_json).is_empty()


def test_get_wishlist_returs_statusCode_404_when_invalid_user() :
    USER = 999

    response = requests.get(GET_WISHLIST_URL.format(uid=USER))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.not_found)
    assert response_json['errorcode'] == 30001
    assert response_json['internalLog'] == 'User not found!'


def test_addbooktowishlist_returns_statusCode_400_when_invalid_user():
    BOOK = 1
    USER = 999

    response = requests.post(ADD_WISHLIST_URL.format(uid=USER, bid=BOOK))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.bad_request)
    assert response_json['errorcode'] == 30003
    assert response_json['internalLog'] == 'User not found!'


def test_addbooktowishlist_returns_statusCode_400_when_invalid_book():
    BOOK = 999
    USER = 1

    response = requests.post(ADD_WISHLIST_URL.format(uid=USER, bid=BOOK))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.bad_request)
    assert response_json['errorcode'] == 30003
    assert response_json['internalLog'] == 'Book not found!'


def test_addbooktowishlist_returns_statusCode_400_when_book_exists_in_wishlist():
    BOOK = 1
    USER = 1

    response = requests.post(ADD_WISHLIST_URL.format(uid=USER, bid=BOOK))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.bad_request)
    assert response_json['errorcode'] == 30003
    assert response_json['internalLog'] == 'Book is present in wishlist!'


def test_addbooktowishlist_returns_new_added_book_to_wishlist():
    BOOK = 4
    USER = 1

    # PREP up data
    requests.delete(DELETE_BOOK_URL.format(uid=USER,bid = BOOK))

    currentWishListResponse = requests.get(GET_WISHLIST_URL.format(uid=USER))
    currentWishlistCount = len(currentWishListResponse.json())
    response = requests.post(ADD_WISHLIST_URL.format(uid=USER,bid = BOOK))
    response_json = response.json()
    newWishlistCount = len(response_json)
    wishlistItems = [(data['fkUserId'], data['fkBookId']) for data in response_json]

    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert currentWishlistCount+1 == newWishlistCount
    assert_that(wishlistItems).contains((USER, BOOK))


def test_deletebookfromwishlist_returns_status_400_when_book_notpresent_in_wishlist():
    BOOK = 4
    USER = 1

    #PREP up data
    requests.delete(DELETE_BOOK_URL.format(uid=USER,bid = BOOK))

    response = requests.delete(DELETE_BOOK_URL.format(uid=USER,bid = BOOK))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.bad_request)
    assert response_json['errorcode'] == 30006
    assert response_json['internalLog'] == 'Book not present in wishlist!'


def test_deletebookfromwishlist_returns_updated_wishlist_after_successfull_delete():
    BOOK = 4
    USER = 1

    # PREP up data
    requests.delete(DELETE_BOOK_URL.format(uid=USER, bid=BOOK))
    requests.post(ADD_WISHLIST_URL.format(uid=USER, bid=BOOK))

    currentWishListResponse = requests.get(GET_WISHLIST_URL.format(uid=USER))
    currentWishlistCount = len(currentWishListResponse.json())
    response = requests.delete(DELETE_BOOK_URL.format(uid=USER, bid=BOOK))
    response_json = response.json()
    newWishlistCount = len(response_json)
    wishlistItems = [(data['fkUserId'], data['fkBookId']) for data in response_json]

    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert currentWishlistCount-1 == newWishlistCount
    assert_that(wishlistItems).does_not_contain(USER, BOOK)


def test_emptywishlist_returns_status_400_when_user_invalid():
    USER = 999

    response = requests.delete(EMPTY_WISHLIST_URL.format(uid=USER))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.bad_request)
    assert response_json['errorcode'] == 30008
    assert response_json['internalLog'] == 'User not found!'


def test_emptywishlistst_empties_wishlist():
    USER = 2
    BOOK1 = 1
    BOOK3 = 3

    # PREP up data
    requests.delete(DELETE_BOOK_URL.format(uid=USER, bid=BOOK1))
    requests.delete(DELETE_BOOK_URL.format(uid=USER, bid=BOOK3))
    requests.post(ADD_WISHLIST_URL.format(uid=USER, bid=BOOK1))
    requests.post(ADD_WISHLIST_URL.format(uid=USER, bid=BOOK3))

    response = requests.delete(EMPTY_WISHLIST_URL.format(uid=USER))
    response_json = response.json()

    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert len(response_json) == 0