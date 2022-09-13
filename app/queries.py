# SQL Queries

def get_query( start, end, filter_params={}):

    list_books_query = """
    select
      data.*
    from
      (
    select final.*, ROW_NUMBER () OVER (
        ORDER BY
          final.download_count desc,
          final.id asc
        )
    from (
    select finaldata.* from
    (
    SELECT
      books.id,
      books.download_count,
      books.gutenberg_id,
      books.title,
      (
        SELECT
          ARRAY(
            {authors_subquery}
          )
      ) as author,
      '' as genre,
      (
        select lang.code from (SELECT
          languages.*, language.code
        FROM
          (select * from books_book_languages) as languages
        LEFT JOIN
          (select * from books_language) as language
        ON language.id = languages.language_id) as lang
        WHERE
          lang.book_id = books.id
          AND lang.book_id IS NOT NULL
        LIMIT
          1
      ) as language,
      (
        SELECT
          ARRAY(
            {subjects_subquery}
          )
      ) as subjects,
      (
        SELECT
          ARRAY(
            {bookshelves_subquery}
          )
      ) as bookshelves,
      (
        SELECT
          ARRAY(
            {links_subquery}
          )
      ) as links
    FROM
      books_book AS books)  as finaldata
    """

    authors_subquery = """
    SELECT
      json_build_object(
        'birth_year', authors.birth_year, 'death_year', authors.death_year,
        'name', authors.name
      )
    FROM
      (select a.book_id, b.* from books_book_authors as a left join books_author as b on a.author_id=b.id) as authors
    WHERE
      authors.book_id = books.id
    """

    links_subquery = """
    SELECT
      json_build_object(
        'mime_type', links.mime_type, 'url', links.url
      )
    FROM
      books_format as links
    WHERE
      links.book_id = books.id
    """


    subjects_subquery = """
    SELECT
      subjects.name
    FROM
      (select a.book_id, b.* from books_book_subjects as a left join books_subject as b on a.subject_id=b.id) as subjects
    WHERE
      subjects.book_id = books.id
    """

    bookshelves_subquery = """
    SELECT
      bookshelf.name
    FROM
      (select a.book_id, b.* from books_book_bookshelves as a left join books_bookshelf as b on a.bookshelf_id=b.id) as bookshelf
    WHERE
      bookshelf.book_id = books.id
    """

    links_suffix = ""
    authors_suffix = ""
    subjects_suffix = ""
    bookshelves_suffix = ""

    query_filters = []
    if filter_params.get('gutenberg_id'):
        filter = ["'"+elem.strip()+"'" for elem in filter_params.get('gutenberg_id').split(',')]
        if len(filter) == 1:
            query_filters.append(" finaldata.gutenberg_id = " + filter[0])
        else:
            query_filters.append(" finaldata.gutenberg_id in ("+ ",".join(filter) +")")

    if filter_params.get('language'):
        filter = ["'"+elem.strip()+"'" for elem in filter_params.get('language').split(',')]
        if len(filter) == 1:
            query_filters.append(" finaldata.language = " + filter[0])
        else:
            query_filters.append(" finaldata.language in ("+ ",".join(filter) +")")

    if filter_params.get('title'):
        filter = [elem.strip() for elem in filter_params.get('title').split(',')]
        if len(filter) == 1:
            query_filters.append(" finaldata.title ilike '%" + filter[0] + "%'")
        else:
            query_filters.append(" finaldata.title similar to '%("+"|".join(filter)+")%'")

    if filter_params.get('topic'):
        filter = [elem.strip() for elem in filter_params.get('topic').split(',')]
        if len(filter) == 1:
            subjects_suffix = " AND subjects.name ilike '%" + filter[0] +"%'"
            bookshelves_suffix = " AND bookshelf.name ilike '%" + filter[0] +"%'"
        else:
            subjects_suffix = " AND subjects.name similar to '%("+"|".join(filter)+")%'"
            bookshelves_suffix = " AND bookshelf.name similar to '%("+"|".join(filter)+")%'"
        query_filters.append("(array_length(finaldata.subjects, 1) > 0 OR array_length(finaldata.bookshelves, 1) > 0)")

    if filter_params.get('mime_type'):
        filter = [elem.strip() for elem in filter_params.get('mime_type').split(',')]
        if len(filter) == 1:
            links_suffix = " AND links.mime_type ilike '%" + filter[0] +"%'"
        else:
            links_suffix = " AND links.mime_type similar to '%("+"|".join(filter)+")%'"
        query_filters.append(" array_length(finaldata.links, 1) > 0")

    if filter_params.get('author'):
        filter = [elem.strip() for elem in filter_params.get('author').split(',')]
        if len(filter) == 1:
            authors_suffix = " AND authors.name ilike '%"+ filter[0] +"%'"
        else:
            authors_suffix = " AND authors.name similar to '%("+"|".join(filter)+")%'"
        query_filters.append(" array_length(finaldata.author, 1) > 0")

    # list_books_query += " WHERE finaldata.row_number BETWEEN "+start+" AND "+end
    if len(query_filters)>0:
        list_books_query += " WHERE "
        list_books_query += " AND ".join(query_filters)

    list_books_query = list_books_query.format(
        links_subquery=links_subquery+links_suffix,
        authors_subquery=authors_subquery+authors_suffix,
        subjects_subquery=subjects_subquery+subjects_suffix,
        bookshelves_subquery=bookshelves_subquery+bookshelves_suffix)

    list_books_query += " ) as final) as data WHERE data.row_number BETWEEN "+start+" AND "+end+" ORDER BY data.download_count desc"
    return list_books_query
