// ==========================
// Ajouter un membre
// ==========================
$(document).ready(function() {
    $('#membreForm').submit(function(e) {
        e.preventDefault(); // empêche le rechargement de la page
        let formData = $(this).serialize(); // récupère les données du formulaire

        $.ajax({
            type: 'POST',
            url: '/ajouter_membre',
            data: formData,
            success: function(response) {
                if(response.success){
                    alert('Membre ajouté avec succès !');
                    $('#membreForm')[0].reset(); // réinitialise le formulaire
                    // Optionnel: mettre à jour la liste des membres via AJAX
                    // updateMembreList();
                } else {
                    alert('Erreur: ' + response.message);
                }
            },
            error: function() {
                alert('Une erreur est survenue lors de l\'ajout du membre.');
            }
        });
    });

    // ==========================
    // Enregistrer une dîme
    // ==========================
    $('#dimeForm').submit(function(e) {
        e.preventDefault();
        let formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: '/enregistrer_dime',
            data: formData,
            success: function(response) {
                if(response.success){
                    alert('Dîme enregistrée avec succès !');
                    $('#dimeForm')[0].reset();
                    // Optionnel: mettre à jour la liste des dîmes
                    // updateDimeList();
                } else {
                    alert('Erreur: ' + response.message);
                }
            },
            error: function() {
                alert('Une erreur est survenue lors de l\'enregistrement de la dîme.');
            }
        });
    });

    // ==========================
    // Fonctions optionnelles pour actualiser les tableaux
    // ==========================
    function updateMembreList(){
        $.get('/liste_membre', function(data){
            $('#membreTableBody').html(data); // à compléter côté serveur pour renvoyer tbody
        });
    }

    function updateDimeList(){
        $.get('/liste_dime', function(data){
            $('#dimeTableBody').html(data); // à compléter côté serveur pour renvoyer tbody
        });
    }
});
