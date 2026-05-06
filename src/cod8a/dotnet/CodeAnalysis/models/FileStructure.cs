using Microsoft.CodeAnalysis.CSharp.Syntax;
using System;
using System.Collections.Generic;
using System.Text;

namespace CodeAnalyzer.models
{
    /// <summary>
    /// Represents the structure of a file, including its identifier and associated namespace details.
    /// </summary>
    public class FileStructure
    {
        public int Id { get; set; }
        /// <summary>
        /// <see langword="nameof"/>of the namespace, e.g., <c>MyNamespace</c>.
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Gets or sets the collection of using directives associated with the current context.
        /// </summary>
        public List<UsingDirective> UsingDirectives { get; set; }

        /// <summary>
        /// Gets or sets the collection of classes associated with the current instance.
        /// </summary>
        public List<ClassStructure> Classes { get; set; }

        /// <summary>
        /// Gets or sets the collection of relationships associated with the entity.
        /// </summary>
        public List<RelationShip> Relationships { get; set; }
    }

    /// <summary>
    /// Represents the relationship the file has with other file(s)
    /// </summary>
    /// <param name="Id">Id of the instance</param>
    /// <param name="Type">Type of relationship</param>
    /// <param name="AssociatedItem">Item associated with</param>
    public record RelationShip(int Id, string Type, string AssociatedItem);

    public record UsingDirective(int Id, string Name);


    /// <summary>
    /// Represents a class, including its name and contained methods.
    /// </summary>
    /// <param name="Id"></param>
    /// <param name="Name"> Gets or sets the name associated with the object. </param>
    /// <param name="Methods"> Gets or sets the collection of methods associated with this instance. </param>
    /// <param name="Fields"> Gets or sets the collection of field definitions associated with the structure. </param>
    /// <param name="Type"> Gets or sets the type associated with the current instance. </param>
    /// <param name="Summary"> Gets or sets the summary description for the current object. </param>
    public record ClassStructure(int Id, string Name, List<MethodStructure> Methods, List<FieldStructure> Fields, string Type, string Summary);

    /// <summary>
    /// Represents the metadata for a method, including its name, access modifier, return type, and parameters.
    /// </summary>
    /// <param name="Id"></param>
    /// <param name="Name"> Gets or sets the name associated with the function. </param>
    /// <param name="Modifier"> Gets or sets the modifier associated with the function. </param>
    /// <param name="ReturnType"> Gets or sets the return type associated with the function. </param>
    /// <param name="Parameters"> Gets or sets the collection of parameters associated with the function. </param>
    /// <param name="Summary"> Gets or sets the summary description for the current object. </param>
    /// <remarks>Use this class to describe the signature and characteristics of a method in code analysis,
    /// code generation, or documentation scenarios. The class does not represent the method's implementation or
    /// behavior.</remarks>
    public record MethodStructure(int Id, string Name, string Modifier, string ReturnType, List<ParameterStructure> Parameters, string Summary);



    /// <param name="Id"></param>
    /// <param name="Name"> Gets or sets the name associated with the field. </param>
    /// <param name="Modifier"> Gets or sets the modifier associated with the field. </param>
    /// <param name="Type"> Gets or sets the type associated with the field. </param>
    /// <param name="Summary"> Gets or sets the summary description for the current object. </param>
    public record FieldStructure(int Id, string Name, string Modifier, string Type, string Summary);





    /// <summary>
    /// Represents a parameter definition, including its name, modifier, and type information.
    /// </summary>
    /// <param name="Name"> Gets or sets the name associated with the object. </param>
    /// <param name="Modifier"> Gets or sets the modifier associated with the current instance. </param>
    /// <param name="Type"> Gets or sets the type associated with the current instance. </param>
    /// <param name="Summary"> Gets or sets the summary description for the current object. </param>
    /// <remarks>Use this class to describe parameters for methods, constructors, or other callable members.
    /// The properties provide metadata about the parameter's identifier, its modifier (such as 'ref', 'out', or 'in'),
    /// and its data type.</remarks>
    public record ParameterStructure(string Name, string Modifier, string Type, string Summary);
}
