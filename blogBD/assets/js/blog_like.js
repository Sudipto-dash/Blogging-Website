const likeIcon = document.getElementById('like-icon');
const likeCount = document.getElementById('like-count');


likeIcon.onclick = () => {
    const blogId = likeIcon.getAttribute('data-blog');
    const url = `/like_blog/${parseInt(blogId)}/`;
    //fetch api
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-type': 'applicatin/json'
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data.liked) {
            likeIcon.classList.remove('empty-like');
        }
        else {
            likeIcon.classList.add('empty-like');
        }
        likeCount.innerHTML = data.like_count;
    })
    .catch(error => {
        console.log(error);
    })
}


