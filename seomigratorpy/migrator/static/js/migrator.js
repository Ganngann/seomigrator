
$(document).ready(function () {

    console.log('4############################# Hello, World! #############################')

    let ajaxurl = '/migrator/cron' // /migrator/cron?url_to_index=1&domain=http://exemple.com;
    let restart_delay = 0
    let url_to_index = 0
    let lastAjaxRequestResponseDelay = 0
    let domain = ''
    let urlScanedPerSeconde = 1
    const scanSecondOld = document.querySelector('.scansecondold')
    const scanSecondNew = document.querySelector('.scansecondnew')

    function fetchUrl() {
        let startTime = Date.now() // enregistre le temps de début

        fetch(ajaxurl)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Erreur réseau lors de la requête fetch')
                }
                return response.json()
            })
            .then((data) => {
                console.log(data)
            })
            .catch((error) => {
                console.error('Erreur lors de la récupération des données : ', error)
            })
            .finally(() => {
                let endTime = Date.now() // enregistre le temps de fin
                let thisRequestResponseDelay = endTime - startTime // calcule le temps de réponse

                if (lastAjaxRequestResponseDelay === 0 || thisRequestResponseDelay < lastAjaxRequestResponseDelay) {
                    url_to_index += 1
                    if (restart_delay > 0) {
                        restart_delay -= 100
                    }
                } else if (thisRequestResponseDelay > lastAjaxRequestResponseDelay) {
                    restart_delay += 100
                    if (url_to_index > 1) {
                        url_to_index -= 1
                    }
                }
                urlScanedPerSeconde = url_to_index / (thisRequestResponseDelay / 1000)
                if (urlScanedPerSeconde > 50) {
                    $('#stopScan').prop('checked', true)
                }
                console.log('urlScanedPerSeconde', urlScanedPerSeconde)
                scanSecondOld.innerHTML = urlScanedPerSeconde.toFixed(2) + '/sec'
                scanSecondNew.innerHTML = urlScanedPerSeconde.toFixed(2) + '/sec'

                lastAjaxRequestResponseDelay = thisRequestResponseDelay // met à jour le temps de réponse de la dernière requête
                ajaxurl = '/migrator/cron?url_to_index=' + url_to_index + '&domain=' + encodeURIComponent(domain)
                if (!document.querySelector('#stopScan').checked) {
                    setTimeout(fetchUrl, restart_delay)
                }
            })
    }

    document.querySelectorAll('input[name="btnradio"]').forEach((radio) => {
        radio.addEventListener('change', (e) => {
            // Récupère les éléments span pour scanold et scannew
            const scanOldSpinner = document.querySelector('.scanold')
            const scanNewSpinner = document.querySelector('.scannew')


            // Retire la classe 'spinner-border' des deux éléments span
            scanOldSpinner.classList.remove('spinner-border')
            scanNewSpinner.classList.remove('spinner-border')

            // Ajoute la classe 'visually-hidden' aux deux éléments span pour scansecondold et scansecondnew
            scanSecondOld.classList.add('visually-hidden')
            scanSecondNew.classList.add('visually-hidden')

            if (e.target.id === 'scanOld') {
                domain = document.querySelector('#id_old_domain').value
                // Ajoute la classe 'spinner-border' à l'élément span pour scanold
                scanOldSpinner.classList.add('spinner-border')
                // Retire la classe 'visually-hidden' de l'élément span pour scansecondold
                scanSecondOld.classList.remove('visually-hidden')
            } else if (e.target.id === 'scanNew') {
                domain = document.querySelector('#id_new_domain').value
                // Ajoute la classe 'spinner-border' à l'élément span pour scannew
                scanNewSpinner.classList.add('spinner-border')
                // Retire la classe 'visually-hidden' de l'élément span pour scansecondnew
                scanSecondNew.classList.remove('visually-hidden')
            }

            if (domain !== '') {
                // Mettre à jour l'URL de la requête Ajax
                ajaxurl = '/migrator/cron?url_to_index=' + url_to_index + '&domain=' + encodeURIComponent(domain)
                // Démarrer la requête Ajax
                fetchUrl()
            }
        })
    })
})

