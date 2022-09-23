from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

import dill

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1Q0rhRTnviyd1QUP54KTWb9gmE-kJyU4s3ASP6_2_GpM'


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        print('The title of the document is: {}'.format(document.get('title')))

        doc_content = document.get('body').get('content')

        # save file as is
        with open('data_jar/doc_content.pkl', 'wb') as outp:
            dill.dump(doc_content, outp)


    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
