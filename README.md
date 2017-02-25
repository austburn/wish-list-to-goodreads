# Wish List To GoodReads

I got frustrated this morning when I couldn't import my Amazon Wish List directly in to GoodReads.

This is my hacked-together-Saturday-morning solution.

Get an access key @ [isbndb.com](isbnd.com).

To use the tool:

```bash
pip install -r requirements.txt
./wish_list_to_goodreads --url https://www.amazon.com/gp/registry/wishlist/<id> --access-key <my_access_key>
```

In `out.csv` you'll find the books that were successfully gathered, in `unsuccessful.csv` you'll find the books that were not found via search.

I can't really guarantee this works well... But it does work.

**Note**: Assumes that you have a wish list entirely compromised of books...
