window.addEventListener('load', function() {
    if ('serviceWorker' in navigator) {
	  var serviceWorker = document.querySelector('meta[name="service-worker-js"]').content;
	  navigator.serviceWorker.register(serviceWorker)
	    .then(function(reg) {
			if (!(reg.showNotification)) {
		        alert('Showing Notification is not suppoted in your browser');
		        return;
		    }

		    // Check the current Notification permission.
		    // If its denied, it's a permanent block until the
		    // user changes the permission
		    if (Notification.permission === 'denied') {
		      alert('The Push Notification is blocked from your browser.');
		      return;
		    }

		    // Check if push messaging is supported
		    if (!('PushManager' in window)) {
		      alert('Push Notification is not available in the browser');
		      return;
		    }

		    // We need to subscribe for push notification and send the information to server
		    getSubscription(reg).then(function(subscription) {
    		    // Send the information to the server with fetch API.
  				// the type of the request, the name of the user subscribing,
  				// and the push subscription endpoint + key the server needs
  				// to send push messages

  				var browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase(),
  				  data = {
  				  			status_type: 'subscribe',
  				            subscription: subscription.toJSON(),
  				            browser: browser
  				         };

  				fetch('/webpush/save_information', {
  				  method: 'post',
  				  headers: {'Content-Type': 'application/json'},
  				  body: JSON.stringify(data),
  				  credentials: 'include'
  				});
    		})
    		.catch(function(error) {
    		    console.log('Subscription error.', error)
    		});
	    });
	}
});

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (var i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function getSubscription(reg) {
    return reg.pushManager.getSubscription().then(
        function(subscription) {
          var metaObj, applicationServerKey, options;
          // Check if Subscription is available
          if (subscription) {
            return subscription;
          }

          metaObj = document.querySelector('meta[name="django-webpush-vapid-key"]');
          applicationServerKey = metaObj.content;
          options = {
              userVisibleOnly: true
          };
          if (applicationServerKey){
              options.applicationServerKey = urlB64ToUint8Array(applicationServerKey)
          }
          // If not, register one
          return reg.pushManager.subscribe(options)
        }
      );
}
