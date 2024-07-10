// Variáveis
var chid = document.getElementById('chid');
var chname = document.getElementById('chname');
var churl = document.getElementById('churl');
var logourl = document.getElementById('logourl');
var chgroup = document.getElementById('chgroup')
var btnAddInfo = document.getElementById('addinfo');
var btnLimpar = document.getElementById('limpar');
var btnDownload = document.getElementById('btnDownload');
var infoField = document.getElementById('infofield');

function AddInfo() {
    if (infoField.value == '') {
        infoField.value = '#EXTM3U8\n'
    } else {
        extFormat = `\n#EXTINF:-1 tvg-id="${chid.value}" tvg-logo="${logourl.value}" group-title="${chgroup.value}", ${chname.value}\n${churl.value}\n`;

        infoField.value += extFormat;
        limparCampos();
    }
}

function limparCampos() {
    chid.value = '';
    chname.value = '';
    churl.value = '';
    logourl.value = '';
    chgroup.value = '';
}

function criarBaixarM3u8() {
    const link = document.getElementById('download');
    const file = 'm3u8_maker.m3u8';

    link.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(infoField.value));
    link.setAttribute('download', file);
}

btnAddInfo.addEventListener('click', AddInfo);
btnLimpar.addEventListener('click', limparCampos);
btnDownload.addEventListener('click', criarBaixarM3u8);
