mkdir -p ~/.streamlit/
echo "\
[theme]\n\
base = 'light'\n\
primaryColor = '#437DCE'\n\
[global]\n\
showWarningOnDirectExecution = false\n\
disableWidgetStateDuplicationWarning = true\n\
storeCachedForwardMessagesInMemory = false\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
\n\
" > ~/.streamlit/config.toml