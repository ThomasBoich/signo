(function(q) {
    function CryptographyGost(q) {
        var idleTime = 3000;
        var cadesplugin = new Cryptography.CryptoPro.Cadesplugin(q);

        /**получение списка сертификатов*/
        function _getCertificates() {
            var certificates = [];
            var dateOptions = {
                year: "numeric",
                month: "numeric",
                day: "numeric"
            };
            return cadesplugin
                .Load(idleTime)
                .then(function(x) {
                    return Cryptography.X509Certificate.X509Store.Open(cadesplugin);
                })
                .then(function(store) {
                    return store.Certificates();
                })
                .then(function(collection) {
                    console.log(collection);
                    if (collection && collection.Items) {
                        for (var i = 0; i < collection.Items.length; i++) {
                            var organization = collection.Items[i].SubjectName.match(
                                /O\=(.*?)\,/
                            )
                                ? collection.Items[i].SubjectName.match(/O\=(.*?)\,/)[1]
                                : ""; //;collection.Items[i].SubjectName.split(',')[3].replace('O=','');
                            var name = collection.Items[i].SubjectName.match(/CN\=(.*?)\,/)
                                ? collection.Items[i].SubjectName.match(/CN\=(.*?)\,/)[1]
                                : "";
                            certificates.push({
                                thumbprint: collection.Items[i].Thumbprint,
                                serial: collection.Items[i].SerialNumber,
                                selectValue: name + " " + organization, //collection.Items[i].SubjectName,
                                subject: collection.Items[i].SubjectName,
                                issuer: collection.Items[i].IssuerName,
                                from: new Date(
                                    collection.Items[i].ValidFromDate
                                ).toLocaleString("ru", dateOptions),
                                expiration: new Date(
                                    collection.Items[i].ValidToDate
                                ).toLocaleString("ru", dateOptions)
                            });
                        }
                    }
                    return certificates;
                });
        }

        /**Подписание*/
        function _sign(thumbprint, content, detached) {
            var certificate;
            return _findCertificateByThumbprint(thumbprint)
                .then(function(x) {
                    certificate = x[0];
                    return Cryptography.Pkcs.CmsSigner.Create(cadesplugin);
                })
                .then(function(signer) {
                    return signer.ComputeSignature(content, certificate, detached);
                })
                .then(function(signature) {
                    return signature;
                })
                .catch(function(ex) {
                    console.error(ex);
                    alert(ex.message || ex);
                });
        }

        /**Паралельное подписание
         * thumbprint - отпечаток сертификата, которым надо подписать
         * content - уже подписанное сообщение
         */
        function _coSign(thumbprint, content) {
            var certificate;
            return _findCertificateByThumbprint(thumbprint)
                .then(function(x) {
                    certificate = x[0];
                    return Cryptography.Pkcs.SignedCms.Create(cadesplugin, content, {
                        ContentEncoding: 1
                    });
                })
                .then(function(signedCms) {
                    return signedCms.CoSign(certificate);
                })
                .then(function(signature) {
                    return signature;
                })
                .catch(function(ex) {
                    console.error(ex);
                    alert(ex.message || ex);
                });
        }

        /**Поиск сертификата в хранидище по его отпечатку*/
        function _findCertificateByThumbprint(thumbprint) {
            var certificates;
            return cadesplugin
                .Load(this.idleTime)
                .then(function(x) {
                    return Cryptography.X509Certificate.X509Store.Open(cadesplugin);
                })
                .then(function(store) {
                    return store.Certificates();
                })
                .then(function(collection) {
                    certificates = collection.Find(
                        thumbprint,
                        Cryptography.X509Certificate.X509CertificateFind.Thumbprint
                    );
                    return certificates;
                });
        }

        /**Вернет статус плагина
         * @param idleTime - параметр загружки, необходимы браузеру для загрузки плагина в память процесса
         *
         */
        function _getState(idleTime) {
            idleTime = idleTime || 1000;
            let rstate = {
                /**Признак установленного плагина */
                isInstalled: false,
                /**Признак того что плагин заблоикирован (характерно для NPAPI версии плагина) */
                isLocked: false,
                isNPAPIDisabled: false,
                /**Описание установленного CSP */
                cryptoProvider: null,
                /**Признак наличия установленного криптопровайдера */
                hasCryptoProvider: false,
                /**Версия установленногоплагина */
                pluginVersion: null
            };
            console.log(cadesplugin);
            return cadesplugin
                .GetPluginState(idleTime)
                .then(function(state) {
                    rstate.isInstalled = state.isInstall;
                    rstate.isLocked = state.isLocked;
                    return rstate;
                })
                .then(function(rstate) {
                    if (rstate.isInstalled && !rstate.isLocked) {
                        return cadesplugin
                            .Load()
                            .then(function() {
                                return cadesplugin.About();
                            })
                            .then(function(about) {
                                rstate.pluginVersion.majorVersion = about.MajorVersion;
                                rstate.pluginVersion.minorVersion = about.MinorVersion;
                                rstate.pluginVersion.buildVersion = about.BuildVersion;
                                return about.ProviderVersion();
                            })
                            .then(function(csp) {
                                if (csp) {
                                    rstate.hasCryptoProvider = true;
                                    rstate.cryptoProvider = {
                                        version: csp
                                    };
                                }
                                return rstate;
                            });
                    }
                    return rstate;
                })
                .then(function() {
                    return rstate;
                })
                .catch(function(ex) {
                    return rstate;
                });
        }

        return {
            getCertificates: _getCertificates,
            sign: _sign,
            coSign: _coSign,
            findCertificateByThumbprint: _findCertificateByThumbprint,
            getState: _getState
        };
    }

    window.cryptography = new CryptographyGost(q);
})(Q);
