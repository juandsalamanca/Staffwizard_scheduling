def eliminate_empty_posts(posts):
  clean_posts = posts
  i=0
  l = len(clean_posts)
  while i < l:
    for post_id in clean_posts:
      if len(clean_posts[post_id])==0:
        del clean_posts[post_id]
        l = len(clean_posts)
        i=0
        break
      i+=1
  return clean_posts
