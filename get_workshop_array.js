const f = () => {
    var elems =  document.querySelector("#profileBlock > div.detailBox > div.collectionChildren").childElements().filter(elem => elem.nodeName == 'DIV')
    elems.shift()
    const luaStr = elems.reduce((acc, val, idx) => {
      const title = val.innerText.split('\n')[0]
      const steamId = val.id.split('_')[1]
      const prefix = idx == 0 ? '' : `${acc},\n`
      return `${prefix}["${title}"] = ${steamId}`
    }, '')
    return luaStr
  }; f();