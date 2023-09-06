//
//  receipts.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-16.
//

import Foundation

class APIService {
    static let shared = APIService() // singleton instance
    
    func fetchReceipts(completion: @escaping (Result<[Receipt], Error>) -> Void) {
        guard let url = URL(string: "http://192.168.2.18:8000/receipts") else {
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                print("error in deconding data")
                return
            }
            
            if let data = data {
                do {
                    let receipts = try JSONDecoder().decode([Receipt].self, from: data)
                    completion(.success(receipts))
                }
                catch {
                    completion(.failure(error))
                }
            }
        }.resume()
    }
    
    func saveReceipt(receipt: Receipt) {
        // TODO save the receipt to the db
        guard let url = URL(string: "http://192.168.2.18:8000/receipts/") else {
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // save the receipt
        do {
            
            // encode the receipt data
            let jsonData = try JSONEncoder().encode(receipt)
            request.httpBody = jsonData
            
            // try to make a post request
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error trying to make a post request using url \(url): \(error)")
                    return
                }
                
                if let data = data {
                    do {
                        let responseModel = try JSONSerialization.jsonObject(with: data, options: [])
                        print("response model: \(responseModel)")
                    }
                    catch {
                        print("error decoding json: \(error)")
                    }
                }
            }.resume()
        }
        catch {
            print("Error saving the receipt: \(error)")
        }
    }
    
    func fetchSearchResult(searchStr: String, completion: @escaping (Result<[Receipt], Error>) -> Void) {
        guard let baseUrl = URL(string: "http://192.168.2.18:8000/search") else {
            print("error: could not create the url")
            return
        }
        
        // query items allows us to build url safely
        var components = URLComponents(url: baseUrl, resolvingAgainstBaseURL: false)!
        components.queryItems = [
            URLQueryItem(name: "query_str", value: searchStr)
        ]
        
        guard let url = components.url else {
            print("error: could not build the url")
            return
        }

        // Create a GET request with the constructed URL
        var request = URLRequest(url: url)
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let error = error {
                print("Error while getting the search result: \(error)")
                completion(.failure(error))
                return
            }
            
            if let data = data {
                // Process the response data here
                
                do {
                    let search_result = try JSONDecoder().decode([Receipt].self, from: data)
                    completion(.success(search_result))
                }
                catch {
                    print("Could not process the search result: \(error)")
                    completion(.failure(error))
                }
            }
        }
        .resume()

    }
}
