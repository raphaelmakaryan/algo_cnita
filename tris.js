const fs = require('fs');

function loadCSV(csv) {
    const contenu = fs.readFileSync(csv, 'utf8');
    const lines = contenu.split(/\r?\n/);
    const result = [];
    const headers = [
        'EU_circo', 'code_region', 'region', 'chef_lieu', 'num_dpt', 'nom_ddpt',
        'pref', 'num_circ', 'nom_commune', 'codes_postaux', 'code_insee',
        'latitude', 'longitude', 'dist'
    ];

    for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        const values = line.split(';');
        const obj = {};

        for (let j = 0; j < headers.length; j++) {
            obj[headers[j]] = values[j];
        }

        result.push(obj.code_insee);
    }
    return result;
}

function tri_insertion(array) {
    for (let index = 0; index < array.length; index++) {
        let j = index;
        while (j > 0 && array[j - 1] > array[j]) {
            const temp = array[j];
            array[j] = array[j - 1];
            array[j - 1] = temp;
            j = j - 1;
        }
    }
    console.log(array);
    console.log("Fin de tri_insertion")
}

function tri_selection_sort(array) {
    for (let index = 0; index < array.length; index++) {
        let min = index;
        for (let j = index + 1; j < array.length; j++) {
            if (array[j] < array[min]) {
                min = j;
            }
        }

        if (min !== index) {
            const arrayTempo = array[index];
            array[index] = array[min];
            array[min] = arrayTempo;
        }
    }
    console.log(array);
    console.log("Fin de tri_selection_sort");
}

function bubble_sort(array) {
    let passage = 0, permutation = true
    while (permutation) {
        permutation = false
        for (let index = 0; index < (array.length - 1); index++) {
            if (array[index] > array[index + 1]) {
                array[index] = array[index + 1]
                array[index + 1] = array[index]
                permutation = true
            }
            passage = passage + 1
        }
    }
    console.log(array);
    console.log("Fin de bubble_sort");
}


const dataArray = loadCSV("./datas/small.csv")
/*
tri_insertion(dataArray)
tri_selection_sort(dataArray)
*/
bubble_sort(dataArray)