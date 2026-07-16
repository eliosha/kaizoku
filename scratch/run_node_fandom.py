import json
import subprocess

# We will run a node one-liner to log the matching items
cmd = [
    "node", "-e",
    """
    global.window = { location: { pathname: '', href: '' } };
    global.localStorage = { getItem: () => null, setItem: () => null };
    global.document = { addEventListener: () => {}, documentElement: { classList: { remove: () => {}, add: () => {} } } };
    require('./main.js');
    
    const fandomSeries = [
      'marvel', 'dc', 'harry potter', 'breaking bad', 'game of thrones', 
      'stranger things', 'peaky blinders', 'the godfather', 'invincible'
    ];
    
    let items = Object.keys(window.productsDB).map(key => ({
      id: key,
      ...window.productsDB[key]
    })).filter(item => {
      const seriesLower = (item.series || '').toLowerCase();
      return fandomSeries.indexOf(seriesLower) !== -1;
    });
    
    console.log('Total matches:', items.length);
    items.forEach((item, idx) => {
      console.log(`${idx + 1}. Key: ${item.id}, Series: ${item.series}, Cat: ${item.category}`);
    });
    """
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
print("STDERR:")
print(res.stderr)
