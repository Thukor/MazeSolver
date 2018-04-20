/*
 * Copyright (C) 2016 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.google.android.cameraview.demo;

import static android.util.Base64.NO_WRAP;

import android.os.AsyncTask;
import android.util.Base64;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

class HttpURLConnector extends AsyncTask<String, File, Void> {
    private final String USER_AGENT = "Mozilla/5.0";

    /**
     *
     * @param image
     * @effects encode the image into a string of bytes that is to be sent to the server to be decoded
     *          and processes
     * @return  string of Base64 encoding of the image
     * @throws Exception
     */
    public static String imageToBytes(File image) throws Exception {
        String imageString = null;
        try {
            FileInputStream fis = new FileInputStream(image);
            byte byteArray[] = new byte[(int) image.length()];
            fis.read(byteArray);
            imageString = Base64.encodeToString(byteArray, NO_WRAP);
            fis.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return imageString;
    }

    /**
     *
     * @param urlParameters
     * @effects sends the encaded Base64 image to a server for processing
     * @return the encoded Base64 of the processed image
     * @throws Exception
     */
    // HTTP POST request
    protected String sendPost(String urlParameters) throws Exception {

        String url = "http://72.224.10.212:1080/solve";
        URL obj = new URL(url);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();

        //add request header
        con.setRequestMethod("POST");
        con.setRequestProperty("User-Agent", USER_AGENT);
        con.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

        // Send post request
        con.setDoOutput(true);
        DataOutputStream wr = new DataOutputStream(con.getOutputStream());
        wr.writeBytes(urlParameters);
        wr.flush();
        wr.close();

        int responseCode = con.getResponseCode();
        System.out.println("\nSending 'POST' request to URL : " + url);
        System.out.println("Post parameters : " + urlParameters);
        System.out.println("Response Code : " + responseCode);

        BufferedReader in = new BufferedReader(
                new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuffer response = new StringBuffer();

        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        //print result
        System.out.println(response.toString());

        return response.toString();
    }

    @Override
    protected Void doInBackground(String... strings) {
        return null;
    }

}
