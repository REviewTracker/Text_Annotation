openai.api_key = ""


def Annotate_data(df):

    results = []
    temp = []
    df1 = pd.DataFrame()
    content = []
    label = []

    temperature_values = [0.25]

    for temperature in temperature_values:
      for text in df['Text']:



        # we add delay to avoid having the model overloaded


        prompt = f"Please classify the following headline as either sarcastic or not sarcastic. Provide only the classification label without any explanation. :\n{text}\n"

        messages = [{"role": "user", "content": prompt}]

        retries = 5
        while retries > 0:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    max_tokens=50,
                    n=1,
                    stop=None,
                    temperature=temperature,
                )

                output = response['choices'][0]['message']['content'].strip()
                results.append(output)
                temp.append(temperature)
                content.append(text)
                label.append(df['Label'].loc[df['Text'] == text].values[0])


                break  # Exit the retry loop if the request is successful
            except openai.error.OpenAIError as e:
                print(f"Error: {e}")
                retries -= 1
                time.sleep(10)  # Wait for 5 seconds before retrying
    # Add the results as a new column to the DataFrame



    df1['Text'] = content
    df1['Label'] = label
    df1['GPTLabel'] = results
    df1['temp'] = temp

    return df1


results = Annotate_data(df)
