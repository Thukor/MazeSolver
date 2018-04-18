import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.Base64;

public class HttpURLConnectionExample {

	private final String USER_AGENT = "Mozilla/5.0";

	public static void main(String[] args) throws Exception {

		HttpURLConnectionExample http = new HttpURLConnectionExample();

		System.out.println("Testing 1 - Send Http GET request");
		http.sendGet();

		System.out.println("Testing 2 - Send Http POST request");
		http.sendPost(imageToBytes());

	}

	private static String imageToBytes() throws Exception
	{

		//encode image to Base64 String
		File f = new File("maze_square_medium.jpg");		//change path of image according to you
		FileInputStream fis = new FileInputStream(f);
		byte byteArray[] = new byte[(int)f.length()];
		fis.read(byteArray);
		String imageString = Base64.getEncoder().encodeToString(byteArray);

		fis.close();

		return imageString;
	}

	private void bytesToImage(String bytes) throws Exception
	{

		//decode Base64 String to image
		FileOutputStream fos = new FileOutputStream("recieved.png"); //change path of image according to you
		byte byteArray[] = Base64.getDecoder().decode(bytes.getBytes());
		fos.write(byteArray);

		fos.close();
	}

	// HTTP GET request
	private void sendGet() throws Exception {

		String url = "http://72.224.10.212:1080/hello";

		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

		// optional default is GET
		con.setRequestMethod("GET");

		//add request header
		con.setRequestProperty("User-Agent", USER_AGENT);

		int responseCode = con.getResponseCode();
		System.out.println("\nSending 'GET' request to URL : " + url);
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

	}

	// HTTP POST request
	private void sendPost(String urlParameters) throws Exception {

		String url = "http://72.224.10.212:1080/solve";
		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();

		//add reuqest header
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

		bytesToImage(response.toString());
	}

}
