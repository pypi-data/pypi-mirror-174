
export const resolveUrl = (url: string) => {
  let currentUrl: string = window.location.href;

  //Cut the notebook
  if (currentUrl.endsWith('.ipynb')) {
    const lastIndex = currentUrl.lastIndexOf('/');
    currentUrl = currentUrl.slice(0, lastIndex);
  }

  currentUrl = currentUrl.replace('/lab', '');

  //replace part of url if extension is used in nbclassic (legacy)
  if (currentUrl.includes('/notebooks/')) {
    currentUrl = currentUrl.replace('notebooks', 'tree');
  }
  //if path is absolute ignore current notebook position
  if (url.startsWith('/')) {
    return currentUrl.slice(0, currentUrl.indexOf('tree')) + 'tree' + url;
  }

  const folders = url.split('/');
  for (const f of folders) {
    if (f === '..') {
      const lastIndex = currentUrl.lastIndexOf('/');
      currentUrl = currentUrl.slice(0, lastIndex);
    } else {
      currentUrl = currentUrl.concat('/' + f);
    }
  }

  console.log(currentUrl);
  return currentUrl;
};
